import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjetDjango1.settings')

app = Celery('ProjetDjango1')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True


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