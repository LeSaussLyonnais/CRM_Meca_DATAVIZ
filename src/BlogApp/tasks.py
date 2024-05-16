# C'est là que l'on gère les tâches éxécutées par Celery
from asgiref.sync import async_to_sync

from django.forms.models import model_to_dict

from celery import shared_task
from channels.layers import get_channel_layer

import requests


from .models import * # Parce que l'on veut sauvegarder la data récupérée par la tâche dans la base de donnée dans notre modèle Weather

#from .pypyodbcCRM import * 
import pypyodbc
import pandas as pd
import os
import subprocess

channel_layer = get_channel_layer()

from .models import Weather, PlanChargeAtelier, Site, Poste, Charge # Parce que l'on veut sauvegarder la data récupérée par la tâche dans la base de donnée dans notre modèle Weather
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
    database = 'BAC_A_SABLE'
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

        # Créer le Poste correspondant
        poste, poste_created = Poste.objects.get_or_create(
            COFRAIS=chrg['cofrais'],
            #DESIGN=chrg['design'],
            #VAR_AFF=1,  # On suppose que VAR_AFF est toujours vrai pour un nouveau poste
            Site_ID=site
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
        charge_obj.save() # Pour sauvegarder les objets dans la base de donnée via nos modèles 'PlanChargeAte


# from .views import site,semaine,atelier,annee

# @shared_task # Pour indiquer à Celery que c'est la tâche à éxecuter en backgroud
# def get_plancharge_data_mdb():
#     global site,semaine,atelier,annee
    
#     resultats = PlanChargeAtelier.objects.filter(COSECT__startswith=site, ANNEE=annee, SEMAINE=semaine, DESIGN__icontains=atelier).values('COSECT', 'ANNEE', 'SEMAINE', 'COFRAIS', 'DESIGN', 'VDUREE')

#     charges = list(resultats)

#     async_to_sync(channel_layer.group_send)('charge', {'type': 'send_new_data', 'text': charges})