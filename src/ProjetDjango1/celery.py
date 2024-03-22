import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjetDjango1.settings')

app = Celery('ProjetDjango1')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Paramétrage de la périodicité d'éxecution des tâches par Celery
app.conf.beat_schedule = {
    'get_weather_data_10s':  {
        'task': 'BlogApp.tasks.get_weather_data',
        'schedule': 10.0
    }
}

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True