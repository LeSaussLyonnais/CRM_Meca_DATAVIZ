# C'est là que l'on gère les tâches éxécutées par Celery
from asgiref.sync import async_to_sync

from django.forms.models import model_to_dict

from celery import shared_task
from channels.layers import get_channel_layer

import requests

from .models import Weather # Parce que l'on veut sauvegarder la data récupérée par la tâche dans la base de donnée dans notre modèle Weather

from .pypyodbcCRM import * 
import pandas
import os
import subprocess

channel_layer = get_channel_layer()


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

    async_to_sync(channel_layer.group_send)('weathers', {'type': 'send_new_data', 'text': weathers})


@shared_task # Pour indiquer à Celery que c'est la tâche à éxecuter en backgroud
def get_plancharge_data():
    os.environ['ODBCINI'] = '/etc/odbc.ini'

    # Define the Components of the Connection String.
    server = '192.168.0.21'
    port = '4900'
    database = 'BAC_A_SABLE'
    username = 'admin'
    password = 'Clip_SERENA'
    MyDataSource = 'hyperfile'
    
    # Utilisez le nom du pilote défini dans odbc.ini
    driver_name = 'HFSQL'

    # Create a connection object.
    connection_object: Connection = connect('DSN='+MyDataSource+'; \
                            UID=' + username + '; \
                            PWD=' + password)
                            
                            #Server Name =' + server + '; \
                            #Server Port=' + port + '; \
                            #DATABASE=' + database + '; \

    cursor_object: Cursor = connection_object.cursor()

    table_name = 'CHARGES'
    table_name_2 = 'CFRAIS'
    site = 'ATCRM'
    atelier = 'TOUR'
    annee = '2024'
    semaine = '12'

    # Define the Select Query.
    sql_select = "SELECT "+table_name+".COSECT, "+table_name+".ANNEE, "+table_name+".SEMAINE, "+table_name+".COFRAIS, "+table_name_2+".DESIGN, "+table_name+".VDUREE  \
                    FROM "+table_name+" LEFT JOIN "+table_name_2+" ON "+table_name+".COFRAIS = "+table_name_2+".COFRAIS \
                    WHERE COSECT like '"+site+"' AND ANNEE = "+annee+" AND SEMAINE = "+semaine+" AND "+table_name_2+".DESIGN like '%"+atelier+"%'"
    cursor_object.execute(sql_select)

    # Define the column names.
    #columns = [column[0] for column in cursor_object.statistics]
    columns = [column[0] for column in cursor_object.description]

    # Execute the Query.
    records = cursor_object.fetchall()

    # Dump to a Pandas DataFrame.
    donnees_affaires = pandas.DataFrame.from_records(
        data=records,
        columns=columns
    )

    # Convertir le DataFrame en un dictionnaire de groupes de données.
    grouped_data = donnees_affaires.groupby(["cosect", "annee", "semaine"])

    # Créer une liste de dictionnaires JSON avec la structure requise.
    json_data = []
    for (cosect, annee, semaine), group in grouped_data:
        postes = []
        for index, row in group.iterrows():
            poste = {
                "cofrais": row["cofrais"].strip(),  # Supprimer les espaces avant et après le code de frais
                "design": row["design"],
                "vduree": row["vduree"]
            }
            postes.append(poste)
        data_entry = {
            "cosect": cosect,
            "annee": int(annee),  # Convertir en entier
            "semaine": int(semaine),  # Convertir en entier
            "postes": postes
        }
        json_data.append(data_entry)

    # Charger la chaîne JSON en tant qu'objet JSON
    #data = json.loads(json_data)

    async_to_sync(channel_layer.group_send)('json_data', {'type': 'send_new_data', 'text': json_data})


@shared_task # Pour indiquer à Celery que c'est la tâche à éxecuter en backgroud
def get_plancharge_data_php():
    #drivers = drivers()
    #for driver in drivers:
    #    print(driver)
    
    # Chemin vers le script PHP que vous souhaitez exécuter
    chemin_script_php = "./Test_query_HFSQL.php"
    chemin_php = "/usr/local/lib/php-8.3.6/php.exe"

    
    # Exécuter le script PHP et capturer la sortie
    #subprocess.call([chemin_php, chemin_script_php])
    resultat = subprocess.check_output([chemin_php, chemin_script_php])

    # Afficher le résultat
    print(resultat.decode("utf-8"))  # Assurez-vous de décoder la sortie en tant que chaîne Unicode si nécessaire
