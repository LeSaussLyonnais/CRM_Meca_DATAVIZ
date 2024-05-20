import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjetDjango1.settings')

app = Celery('ProjetDjango1')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Paramétrage de la périodicité d'éxecution des tâches par Celery
'''
app.conf.beat_schedule = {
    'get_weather_data_10s':  {
        'task': 'BlogApp.tasks.get_weather_data',
        'schedule': 10.0
    }
}
'''

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True

valeur_de_x = 0

def obtenir_valeur_de_x():
    # Cette fonction peut être définie dans n'importe quelle partie de votre code
    # Elle peut déterminer la valeur de x en fonction de certaines conditions ou de l'état de votre application
    
    result = valeur_de_x
    return result  # Exemple de valeur pour x


app.conf.beat_schedule = {
    'get_plancharge_data_erp_300s': {
        'task': 'BlogApp.tasks.get_plancharge_data_erp',
        'schedule': 300.0
        #'args': (obtenir_valeur_de_x(),),  # Appel de la fonction pour obtenir la valeur de x
    }
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')