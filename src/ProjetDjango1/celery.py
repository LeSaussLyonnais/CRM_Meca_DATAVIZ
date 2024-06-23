import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjetDjango1.settings')

app = Celery('ProjetDjango1')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True


app.conf.beat_schedule = {
    'get_plancharge_data_erp_15min': {
        'task': 'BlogApp.tasks.get_plancharge_data_erp',
        'schedule': 1000.0,
        # 'schedule': crontab(minute='*/15')  # Toutes les 5 minutes
    },
    'get_ordo_data_erp_15min': {
        'task': 'BlogApp.tasks.get_ordo_data_erp',
        'schedule': 1000.0,
        # 'schedule': crontab(minute='*/5')  # Toutes les 5 minutes
    },
    'get_last10of_data_erp_15min': {
        'task': 'BlogApp.tasks.get_last10of_data_erp',
        'schedule': 1000.0,
        # 'schedule': crontab(minute='*/5')  # Toutes les 5 minutes
    }
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')