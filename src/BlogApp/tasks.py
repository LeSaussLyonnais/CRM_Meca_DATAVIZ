# C'est là que l'on gère les tâches éxécutées par Celery
from asgiref.sync import async_to_sync

from django.forms.models import model_to_dict

from celery import shared_task
from channels.layers import get_channel_layer

import requests

from .models import Weather # Parce que l'on veut sauvegarder la data récupérée par la tâche dans la base de donnée dans notre modèle Weather


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