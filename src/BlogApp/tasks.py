# C'est là que l'on gère les tâches éxécutées par Celery
from asgiref.sync import async_to_sync

from django.forms.models import model_to_dict
from django.utils.dateformat import format
from django.utils.timezone import make_aware
from django.db.models import F, Value, IntegerField, ExpressionWrapper, Q
from django.db.models.functions import Coalesce
from celery import shared_task
from channels.layers import get_channel_layer

import requests

#from .pypyodbcCRM import * 
import pypyodbc
import pandas as pd
import datetime
from datetime import date
import os
import subprocess

channel_layer = get_channel_layer()

from .models import * # Parce que l'on veut sauvegarder la data récupérée par la tâche dans la base de donnée dans notre modèle Weather

@shared_task # Pour indiquer à Celery que c'est la tâche à éxecuter en backgroud
def get_weather_data():
    url = 'https://api.openweathermap.org/data/2.5/forecast?lat=43.60&lon=1.433333&appid=86a1d03a37f156f8b34f6be197056295&units=metric'
    #url = 'https://api.openweathermap.org/data/2.5/weather?lat=43.60&lon=1.433333&appid=86a1d03a37f156f8b34f6be197056295'
    # Faut que je prenne une API qui me donne une liste de résultats pas juste les donnée d'un lieu à un seul instant
    open_weather_data = requests.get(url).json()
    data = open_weather_data["list"]
    #data_wthr = data['weather']

    weathers = [] # On défini une liste de météos (par lieu)

    for wthr in data:
        obj, created = Weather.objects.get_or_create(dt_txt=wthr['dt_txt']) # "dt_txt=wthr['dt_txt']"

        
        obj.dt_txt = wthr['dt_txt']
        
        
        if obj.temp > wthr['main'].get('temp'):
            state = 'fall'
        elif obj.temp == wthr['main'].get('temp'):
            state = 'same'
        elif obj.temp < wthr['main'].get('temp'):
            state = 'raise'
        
        obj.temp = wthr['main'].get('temp') # Là on fait un .get('xxx') parceque la clé 'main' n'est pas une liste dans le JSON

        obj.icon = wthr['weather'][0]['icon'] # Là on fait un [0]['xxx'] parceque la clé 'weather' est une liste dans le JSON
        
        
        #obj.dt = wthr['dt']
        #for wthr in data_wthr:
        #    obj.weather = wthr['main']
        
        obj.save() # Pour sauvegarder l'objet 'obj' dans la base de donnée via notre modèle 'Weather'

        new_data = model_to_dict(obj)
        new_data.update({'state': state})

        weathers.append(new_data)
        #print(weathers)

    async_to_sync(channel_layer.group_send)('weathers', {'type': 'send_new_data', 'text': weathers})

@shared_task # Pour indiquer à Celery que c'est la tâche à éxecuter en backgroud
def get_plancharge_data_erp():
    os.environ['ODBCINI'] = '/etc/odbc.ini'

    # Define the Components of the Connection String.
    server = '192.168.0.21'
    port = '4900'
    database = 'ICAM'
    username = 'admin'
    password = 'Clip_SERENA'
    #MyDataSource = 'hyperfile'
    
    # Utilisez le nom du pilote défini dans odbc.ini
    driver_name = 'HFSQL'

    # Create a connection object.
    connection_object: pypyodbc.Connection = pypyodbc.connect('DRIVER={HFSQL}; \
                            Server Name =' + server + '; \
                            Server Port=' + port + '; \
                            DATABASE=' + database + '; \
                            UID=' + username + '; \
                            PWD=' + password)
                            
                            #Server Name =' + server + '; \
                            #Server Port=' + port + '; \
                            #DATABASE=' + database + '; \

    cursor_object: pypyodbc.Cursor = connection_object.cursor()

    table_name = 'CHARGES'
    table_name_2 = 'CFRAIS'
    site = 'ATCRM'
    atelier = 'TOUR'
    annee = '2024'
    semaine = '12'

    # Define the Select Query.
    sql_select = "SELECT SECTIONS.LIBELLE, "+table_name+".COSECT, "+table_name+".ANNEE, "+table_name+".SEMAINE, "+table_name+".COFRAIS, "+table_name_2+".DESIGN, "+table_name+".VDUREE  \
                    FROM "+table_name+" LEFT JOIN "+table_name_2+" ON "+table_name+".COFRAIS = "+table_name_2+".COFRAIS \
                        LEFT JOIN SECTIONS ON "+table_name_2+".COSECT = SECTIONS.COSECT"
    cursor_object.execute(sql_select)
    
    # Define the column names.
    #columns = [column[0] for column in cursor_object.statistics]
    columns = [column[0] for column in cursor_object.description]

    # Execute the Query.
    records = cursor_object.fetchall()

    # Dump to a Pandas DataFrame.
    plancharge_df = pd.DataFrame.from_records(
        data=records,
        columns=columns
    )

    charge_liste = plancharge_df.to_dict('records')

    #charges = []
    
    for chrg in charge_liste:
        # Créer ou récupérer le Site correspondant
        site, site_created = Site.objects.get_or_create(
            COSECT=chrg['cosect'],
            #Libelle_Site='libelle'
        )

        site_default, site_default_created = Site.objects.get_or_create(
            COSECT='DEFAULT',
            VAR_AFF_SITE=0
        )

        # Récupérer ou créer l'atelier avec Libelle_Atelier = 'DEFAULT'
        # atelier_default = 'DEFAULT'

        atelier, created = Atelier.objects.get_or_create(
            Libelle_Atelier='DEFAULT',
            VAR_AFF_AT=0
        )

        # Créer le Poste correspondant
        poste, poste_created = Poste.objects.get_or_create(
            COFRAIS=chrg['cofrais'],
            Site_ID=site,
            defaults={
                'Atelier_ID': atelier,
                # 'Site_ID': site_default  # Assurez-vous de toujours fournir un Site_ID
            }
        )
    
        # Créer la Charge correspondante
        charge_obj, pcharge_created = Charge.objects.get_or_create(
            #VDUREE=chrg['vduree'],
            ANNEE=chrg['annee'],
            SEMAINE=chrg['semaine'],
            Poste_ID=poste
        )

        #obj, created = PlanChargeAtelier.objects.get_or_create(COSECT=chrg['cosect'], COFRAIS=chrg['cofrais'], ANNEE=chrg['annee'], SEMAINE=chrg['semaine'])
        site.COSECT = chrg['cosect']
        site.Libelle_Site = chrg['libelle']
        poste.Site_ID = site
        poste.COFRAIS = chrg['cofrais']
        poste.DESIGN = chrg['design']
        charge_obj.Poste_ID = poste
        charge_obj.ANNEE = chrg['annee']
        charge_obj.SEMAINE = chrg['semaine']
        charge_obj.VDUREE = chrg['vduree']
        site.save()
        poste.save()
        charge_obj.save() # Pour sauvegarder les objets dans la base de donnée via nos modèles 'PlanChargeAtelier'


@shared_task # Pour indiquer à Celery que c'est la tâche à éxecuter en backgroud
def get_ordo_data_erp():
    # Define the Components of the Connection String.
    server = '192.168.0.21'
    port = '4900'
    database = 'ICAM'
    username = 'admin'
    password = 'Clip_SERENA'

    # Variables dates
    date_today = datetime.datetime.today()
    formatted_date_today = date_today.strftime('%Y%m%d%H%M%S')
    date_limit = date_today + datetime.timedelta(days=42)
    formatted_date_limit = date_limit.strftime('%Y%m%d')
    print(formatted_date_limit)

    # Create a connection object.
    connection_object: pypyodbc.Connection = pypyodbc.connect('DRIVER={HFSQL}; \
                            Server Name =' + server + '; \
                            Server Port=' + port + '; \
                            DATABASE=' + database + '; \
                            UID=' + username + '; \
                            PWD=' + password)
                            #Trusted_Connection=yes;

    # Create a Cursor Object, using the connection.
    cursor_object: pypyodbc.Cursor = connection_object.cursor()

    # Define the Select Query.
    sql_select = "SELECT GAMME.GACLEUNIK, \
                    CHARGE.DAT as DATE_CHARGE, \
                    CHARGRES.DAT as DATE_ORDO, \
                    CHARGRES.HEUREDEB as HEURE_ORDO, \
                    CLIENT.NOM as CLIENT_NOM, \
                    AFFAIRE.NAF, \
                    AFFAIRE.ETATAF, \
                    GAMME.RANG, \
                    GAMME.EN_PIECE, \
                    GAMME.PHASE, \
                    AFFAIRE.QTEAF, \
                    AFFAIRE.QTEAFREST, \
                    GAMME.GA_PREP, \
                    GAMME.GA_NBH, \
                    GAMME.GA_NBHR, \
                    AFFAIRE.TYPEAF, \
                    GAMME.OPFINIE, \
                    GAMME.COFRAIS, \
                    CHARGE.COSECT \
                    FROM GAMME \
                    LEFT JOIN AFFAIRE ON GAMME.NAF = AFFAIRE.NAF \
                    LEFT JOIN ENGAM ON GAMME.ENCLEUNIK = ENGAM.ENCLEUNIK \
                    LEFT JOIN CLIENT ON AFFAIRE.COCLI = CLIENT.COCLI \
                    LEFT JOIN CHARGRES ON GAMME.GACLEUNIK = CHARGRES.GACLEUNIK \
                    LEFT JOIN CHARGE ON GAMME.GACLEUNIK = CHARGE.GACLEUNIK \
                    WHERE AFFAIRE.TYPEAF = 1 \
                    AND DATE_CHARGE >= '"+formatted_date_today+"' \
                    AND DATE_CHARGE <= '"+formatted_date_limit+"'" # Voir pour enlever la borne inférieure en prod sur BDD CRM et mettre DATE_CHARGE IS NOT NULL
    cursor_object.execute(sql_select)

    # Define the column names.
    #columns = [column[0] for column in cursor_object.statistics]
    columns = [column[0] for column in cursor_object.description]

    # Execute the Query.
    # records = cursor_object.fetchmany(10)
    records = cursor_object.fetchall()

    # Dump to a Pandas DataFrame.
    ordo_df = pd.DataFrame.from_records(
        data=records,
        columns=columns,
    )

    # Localiser en UTC
    # ordo_df['dateordoold'] = ordo_df['dateordoold'].dt.tz_localize('UTC', ambiguous='NaT', nonexistent='shift_forward')

    # Traiter les valeurs NaT avant d'utiliser le DataFrame
    ordo_df['date_charge'] = ordo_df['date_charge'].astype(object).where(ordo_df['date_charge'].notnull(), None)
    ordo_df['date_ordo'] = ordo_df['date_ordo'].astype(object).where(ordo_df['date_ordo'].notnull(), None)
    ordo_df['heure_ordo'] = ordo_df['heure_ordo'].astype(object).where(ordo_df['heure_ordo'].notnull(), None)
    # ordo_df['dateordoold'] = ordo_df['dateordoold'].astype(object).where(ordo_df['dateordoold'].notnull(), None)    

    ordo_liste = ordo_df.to_dict('records')

    for ordo in ordo_liste:
        # Créer le site de défault
        site_default, site_default_created = Site.objects.get_or_create(
            COSECT='DEFAULT',
            VAR_AFF_SITE=0
        )
        
        # Créer ou récupérer le Site correspondant
        site, site_created = Site.objects.get_or_create(
            COSECT=ordo['cosect'],
            #Libelle_Site='libelle'
        )        
        
        atelier, created = Atelier.objects.get_or_create(
            Libelle_Atelier='DEFAULT',
            VAR_AFF_AT=0
        )

        # Créer le Poste correspondant
        poste, poste_created = Poste.objects.get_or_create(
            COFRAIS=ordo['cofrais'],
            Site_ID=site,
            defaults={
                'Atelier_ID': atelier,
                # 'Site_ID': site_default
            }
        )
    
        # Créer la Charge correspondante
        of_obj, of_created = Ordre_Frabrication.objects.get_or_create(
            GACLEUNIK=ordo['gacleunik'],
            DATE_CHARGE=ordo['date_charge'],
            NAF=ordo['naf'],
            RANG=ordo['rang'],
            OF_Poste_ID=poste
        )

        site.COSECT = ordo['cosect']
        poste.COFRAIS = ordo['cofrais']
        of_obj.OF_Poste_ID = poste
        of_obj.GACLEUNIK = ordo['gacleunik']
        of_obj.DATE_CHARGE = ordo['date_charge']
        of_obj.DATE_ORDO = ordo['date_ordo']
        of_obj.HEURE_ORDO = ordo['heure_ordo']
        # of_obj.DATEORDOOLD = ordo['dateordoold']
        of_obj.CLIENT_NOM = ordo['client_nom']
        of_obj.NAF = ordo['naf']
        of_obj.ETATAF = ordo['etataf']
        of_obj.RANG = ordo['rang']
        of_obj.EN_PIECE = ordo['en_piece']
        of_obj.PHASE = ordo['phase']
        of_obj.QTEAF = ordo['qteaf']
        of_obj.QTEAFREST = ordo['qteafrest']
        of_obj.GA_PREP = ordo['ga_prep']
        of_obj.GA_NBH = ordo['ga_nbh']
        of_obj.GA_NBHR = ordo['ga_nbhr']
        of_obj.TYPEAF = ordo['typeaf']
        of_obj.OPFINIE = ordo['opfinie']
        site.save()
        poste.save()
        of_obj.save()


@shared_task # Pour indiquer à Celery que c'est la tâche à éxecuter en backgroud
def get_last10of_data_erp():
    # Define the Components of the Connection String.
    server = '192.168.0.21'
    port = '4900'
    database = 'ICAM'
    username = 'admin'
    password = 'Clip_SERENA'

    # Variables dates
    date_today = datetime.datetime.today()
    date_limit = date_today + datetime.timedelta(days=42)
    formatted_date_limit = date_limit.strftime('%Y%m%d')
    print(formatted_date_limit)

    # Create a connection object.
    connection_object: pypyodbc.Connection = pypyodbc.connect('DRIVER={HFSQL}; \
                            Server Name =' + server + '; \
                            Server Port=' + port + '; \
                            DATABASE=' + database + '; \
                            UID=' + username + '; \
                            PWD=' + password)
                            #Trusted_Connection=yes;

    # Create a Cursor Object, using the connection.
    cursor_object: pypyodbc.Cursor = connection_object.cursor()

    # Define the Select Query.
    sql_select = "SELECT GAMME.GACLEUNIK, \
                    CHARGE.DAT as DATE_CHARGE, \
                    CHARGRES.DAT as DATE_ORDO, \
                    CHARGRES.HEUREDEB as HEURE_ORDO, \
                    GAMME.DATEORDOOLD, \
                    CLIENT.NOM as CLIENT_NOM, \
                    AFFAIRE.NAF, \
                    AFFAIRE.ETATAF, \
                    GAMME.RANG, \
                    GAMME.EN_PIECE, \
                    GAMME.PHASE, \
                    AFFAIRE.QTEAF, \
                    AFFAIRE.QTEAFREST, \
                    GAMME.GA_PREP, \
                    GAMME.GA_NBH, \
                    GAMME.GA_NBHR, \
                    AFFAIRE.TYPEAF, \
                    GAMME.OPFINIE, \
                    GAMME.COFRAIS, \
                    CFRAIS.COSECT \
                    FROM GAMME \
                    LEFT JOIN AFFAIRE ON GAMME.NAF = AFFAIRE.NAF \
                    LEFT JOIN ENGAM ON GAMME.ENCLEUNIK = ENGAM.ENCLEUNIK \
                    LEFT JOIN CLIENT ON AFFAIRE.COCLI = CLIENT.COCLI \
                    LEFT JOIN CHARGRES ON GAMME.GACLEUNIK = CHARGRES.GACLEUNIK \
                    LEFT JOIN CHARGE ON GAMME.GACLEUNIK = CHARGE.GACLEUNIK \
                    LEFT JOIN CFRAIS ON GAMME.COFRAIS = CFRAIS.COFRAIS \
                    WHERE AFFAIRE.TYPEAF = 1 \
                    AND OPFINIE like 'O' \
                    AND GAMME.DATEORDOOLD IS NOT NULL \
                    AND GAMME.DATEORDOOLD <> '00000000000000000' \
                    AND CFRAIS.COSECT IS NOT NULL"
    cursor_object.execute(sql_select)


    # Define the column names.
    #columns = [column[0] for column in cursor_object.statistics]
    columns = [column[0] for column in cursor_object.description]

    # Execute the Query.
    # records = cursor_object.fetchmany(10)
    records = cursor_object.fetchall()

    # Dump to a Pandas DataFrame.
    last10of_df = pd.DataFrame.from_records(
        data=records,
        columns=columns,
    )

    # Localiser en UTC
    last10of_df['dateordoold'] = last10of_df['dateordoold'].dt.tz_localize('UTC', ambiguous='NaT', nonexistent='shift_forward')

    # Traiter les valeurs NaT avant d'utiliser le DataFrame
    last10of_df['date_charge'] = last10of_df['date_charge'].astype(object).where(last10of_df['date_charge'].notnull(), None)
    last10of_df['date_ordo'] = last10of_df['date_ordo'].astype(object).where(last10of_df['date_ordo'].notnull(), None)
    last10of_df['heure_ordo'] = last10of_df['heure_ordo'].astype(object).where(last10of_df['heure_ordo'].notnull(), None)
    last10of_df['dateordoold'] = last10of_df['dateordoold'].astype(object).where(last10of_df['dateordoold'].notnull(), None)    

    last10of_liste = last10of_df.to_dict('records')

    for last10of in last10of_liste:
        # Créer le site de défault
        site_default, site_default_created = Site.objects.get_or_create(
            COSECT='DEFAULT',
            VAR_AFF_SITE=0
        )
        
        # Créer ou récupérer le Site correspondant
        cosect_value = last10of['cosect'] if last10of['cosect'] else 'DEFAULT'
        site, site_created = Site.objects.get_or_create(
            COSECT=cosect_value,
            #Libelle_Site='libelle'
        )        
        
        atelier, created = Atelier.objects.get_or_create(
            Libelle_Atelier='DEFAULT',
            VAR_AFF_AT=0
        )

        # Créer le Poste correspondant
        poste, poste_created = Poste.objects.get_or_create(
            COFRAIS=last10of['cofrais'],
            Site_ID=site,
            defaults={
                'Atelier_ID': atelier,
                # 'Site_ID': site_default
            }
        )
    
        # Créer la Charge correspondante
        of_obj, of_created = Ordre_Frabrication.objects.get_or_create(
            GACLEUNIK=last10of['gacleunik'],
            DATE_CHARGE=last10of['date_charge'],
            DATEORDOOLD=last10of['dateordoold'],
            NAF=last10of['naf'],
            RANG=last10of['rang'],
            OF_Poste_ID=poste,
        )

        site.COSECT = last10of['cosect']
        poste.COFRAIS = last10of['cofrais']
        of_obj.OF_Poste_ID = poste
        of_obj.GACLEUNIK = last10of['gacleunik']
        of_obj.DATE_CHARGE = last10of['date_charge']
        of_obj.DATE_ORDO = last10of['date_ordo']
        of_obj.HEURE_ORDO = last10of['heure_ordo']
        of_obj.DATEORDOOLD = last10of['dateordoold']
        of_obj.CLIENT_NOM = last10of['client_nom']
        of_obj.NAF = last10of['naf']
        of_obj.ETATAF = last10of['etataf']
        of_obj.RANG = last10of['rang']
        of_obj.EN_PIECE = last10of['en_piece']
        of_obj.PHASE = last10of['phase']
        of_obj.QTEAF = last10of['qteaf']
        of_obj.QTEAFREST = last10of['qteafrest']
        of_obj.GA_PREP = last10of['ga_prep']
        of_obj.GA_NBH = last10of['ga_nbh']
        of_obj.GA_NBHR = last10of['ga_nbhr']
        of_obj.TYPEAF = last10of['typeaf']
        of_obj.OPFINIE = last10of['opfinie']
        site.save()
        poste.save()
        of_obj.save()



################################################################################################
############################ Section Taches requete db Django ##################################
################################################################################################

@shared_task(name="get_plancharge_data_mdb") # Pour indiquer à Celery que c'est la tâche à éxecuter en backgroud
def get_plancharge_data_mdb(setup_id):

    setup = Setup.objects.get(id=setup_id)

    # Do heavy computation with variables in setup model here.
    site = setup.nom_site
    atelier = setup.nom_atelier
    annee = setup.num_annee
    semaine = setup.num_semaine

    resultats = Charge.objects.filter(
        SEMAINE=semaine,
        ANNEE=annee,
        Poste_ID__Atelier_ID__Libelle_Atelier=atelier,
        Poste_ID__Site_ID__COSECT=site
    ).select_related('Poste_ID__Atelier_ID', 'Poste_ID__Site_ID').annotate(
        COFRAIS=F('Poste_ID__COFRAIS'),
        DESIGN=F('Poste_ID__DESIGN'),
        Libelle_Atelier=F('Poste_ID__Atelier_ID__Libelle_Atelier'),
        COSECT=F('Poste_ID__Site_ID__COSECT')
    ).values(
        'VDUREE',
        'SEMAINE',
        'ANNEE',
        'COFRAIS',
        'DESIGN',
        'Libelle_Atelier',
        'COSECT'
    )

    charges = list(resultats)

    ch_site = site.strip()
    ch_atelier = atelier.strip()
    ch_annee = str(annee).strip()
    ch_semaine = str(semaine).strip()
    async_to_sync(channel_layer.group_send)(
        "charge_"+ch_site+"_"+ch_atelier+"_"+ch_annee+"_"+ch_semaine, 
        {
            'type': 'send_new_data', 
            'text': charges
        }
    )


@shared_task(name="get_ordo_data_mdb") # Pour indiquer à Celery que c'est la tâche à éxecuter en backgroud
def get_ordo_data_mdb(setup_id):
    try:
        setup_of = Setup_OF.objects.get(id=setup_id)
    except Setup_OF.DoesNotExist:
        logger.error(f"Setup_OF with id {setup_id} does not exist")
        return

    # Do heavy computation with variables in setup model here.
    poste = setup_of.nom_poste

    date_today = datetime.datetime.today()

    # Requête Django ORM
    resultats = Ordre_Frabrication.objects.filter(
        OF_Poste_ID=poste,
        # DATE_ORDO__gt=date_today
    ).exclude(
        Q(DATE_ORDO=None) | Q(DATE_CHARGE=None)
    ).values(
        'GACLEUNIK', 
        'DATE_ORDO', 
        'CLIENT_NOM', 
        'NAF', 
        'ETATAF', 
        'RANG', 
        'EN_PIECE', 
        'PHASE', 
        'QTEAF', 
        # 'GA_PREP', 
        # 'GA_NBH', 
        'GA_NBHR', 
        'TYPEAF'
    ).annotate(
        TOTAL_TEMPS=Coalesce(F('GA_PREP'), Value(0.0)) + Coalesce(F('GA_NBH'), Value(0.0)), # , output_field=FloatField()
        PHASE_AVANT=Value(0, output_field=IntegerField()),
        PHASE_SUIVANTE=Value(0, output_field=IntegerField())
    ).order_by(
        'DATE_ORDO',
        'HEURE_ORDO'
    ).distinct()

    
    
    # Convertir les objets datetime.date et datetime.time en chaînes de caractères
    ordos = list(resultats)
    for ordo in ordos:
        ordo['DATE_ORDO'] = format(ordo['DATE_ORDO'], 'Y-m-d')  # Format ISO 8601 pour la date
        # Si vous avez également besoin de convertir l'heure, utilisez format(ordo['heure_ordo'], 'H:i:s') ou similaire
        
        # Subquery :
        subquery_phase_avant = Ordre_Frabrication.objects.filter(
            NAF=ordo['NAF'],
            PHASE=ordo['PHASE'] - 10
        ).values(
            'OF_Poste_ID'
        )

        # Si vous souhaitez ajouter le résultat de la sous-requête dans 'ordo'
        ordo['PHASE_AVANT'] = subquery_phase_avant[0]['OF_Poste_ID'] if subquery_phase_avant.exists() else None

        # Subquery :
        subquery_phase_suivante = Ordre_Frabrication.objects.filter(
            NAF=ordo['NAF'],
            PHASE=ordo['PHASE'] + 10
        ).values(
            'OF_Poste_ID'
        )

        # Si vous souhaitez ajouter le résultat de la sous-requête dans 'ordo'
        ordo['PHASE_SUIVANTE'] = subquery_phase_suivante[0]['OF_Poste_ID'] if subquery_phase_suivante.exists() else None

    ch_poste = poste.strip()
    async_to_sync(channel_layer.group_send)(
        "ordo_"+ch_poste, 
        {
            'type': 'send_new_data', 
            'text': ordos
        }
    )


@shared_task(name="get_last10OF_data_mdb") # Pour indiquer à Celery que c'est la tâche à éxecuter en backgroud
def get_last10OF_data_mdb(setup_id):
    try:
        setup_last10of = Setup_Last10OF.objects.get(id=setup_id)
    except Setup_OF.DoesNotExist:
        logger.error(f"Setup_OF with id {setup_id} does not exist")
        return

    # Do heavy computation with variables in setup model here.
    poste = setup_last10of.nom_poste

    # Requête Django ORM
    resultats = Ordre_Frabrication.objects.filter(
        OF_Poste_ID=poste,
        OPFINIE='O'
    ).values(
        'NAF',
        'RANG', 
        'PHASE',
        'GA_NBHR',
        'OPFINIE',
        'DATEORDOOLD',
    ).annotate(
        TOTAL_TEMPS=Coalesce(F('GA_PREP'), Value(0.0)) + Coalesce(F('GA_NBH'), Value(0.0)),
    ).order_by(
        '-DATEORDOOLD',
    ).distinct()[:10]

    last10ofs = list(resultats)

    # Convertir les objets datetime en chaînes de caractères
    for of in last10ofs:
        if 'DATEORDOOLD' in of and isinstance(of['DATEORDOOLD'], datetime.datetime):
            of['DATEORDOOLD'] = of['DATEORDOOLD'].isoformat()

    print(last10ofs)

    ch_poste = poste.strip()
    async_to_sync(channel_layer.group_send)(
        "last10of_"+ch_poste, 
        {
            'type': 'send_new_data', 
            'text': last10ofs
        }
    )


@shared_task(name="get_pdc_machine_data_mdb") # Pour indiquer à Celery que c'est la tâche à éxecuter en backgroud
def get_pdc_machine_data_mdb(setup_id):

    setup_pdc_machine = Setup_PDCMachine.objects.get(id=setup_id)

    # Do heavy computation with variables in setup model here.

    poste = setup_pdc_machine.nom_poste
    annee = setup_pdc_machine.num_annee
    semaine_min = setup_pdc_machine.num_semaine
    semaine_max = semaine_min + 6

    resultats = Charge.objects.filter(
        SEMAINE__gte=semaine_min,
        SEMAINE__lte=semaine_max,
        ANNEE=annee,
        Poste_ID=poste,
    ).select_related('Poste_ID__Atelier_ID', 'Poste_ID__Site_ID').annotate(
        COFRAIS=F('Poste_ID__COFRAIS'),
        DESIGN=F('Poste_ID__DESIGN'),
        Libelle_Atelier=F('Poste_ID__Atelier_ID__Libelle_Atelier'),
        COSECT=F('Poste_ID__Site_ID__COSECT')
    ).values(
        'VDUREE',
        'SEMAINE',
        'ANNEE',
        'COFRAIS',
        'DESIGN',
        'Libelle_Atelier',
        'COSECT'
    )

    charges_machine = list(resultats)

    ch_poste = poste.strip()
    ch_annee = str(annee).strip()
    ch_semaine_min = str(semaine_min).strip()
    async_to_sync(channel_layer.group_send)(
        "charge_machine_"+ch_poste+"_"+ch_annee+"_"+ch_semaine, 
        {
            'type': 'send_new_data', 
            'text': charges_machine
        }
    )

    
