import os
from celery import Celery
from celery.schedules import crontab
from kombu import Queue, Exchange


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjetDjango1.settings')

app = Celery('ProjetDjango1')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True


app.conf.beat_schedule = {
    'get_plancharge_data_erp_15min': {
        'task': 'get_plancharge_data_erp',
        'schedule': 900,
        # 'schedule': crontab(minute='*/15')  # Toutes les 5 minutes
    },
    'get_ordo_data_erp_15min': {
        'task': 'get_ordo_data_erp',
        'schedule': 900,
        # 'schedule': crontab(minute='*/5')  # Toutes les 5 minutes
    },
    'get_last10of_data_erp_15min': {
        'task': 'get_last10of_data_erp',
        'schedule': 900,
        # 'schedule': crontab(minute='*/5')  # Toutes les 5 minutes
    }
}

# Define the queues
app.conf.task_queues = (
    Queue('worker1_queue', Exchange('worker1_queue'), routing_key='worker1_queue.#'),
    Queue('worker2_queue', Exchange('worker2_queue'), routing_key='worker2_queue.#'),
)

# Define the default routing for tasks
app.conf.task_routes = {
    'get_plancharge_data_erp': {'queue': 'worker1_queue'},
    'get_ordo_data_erp': {'queue': 'worker1_queue'},
    'get_last10of_data_erp': {'queue': 'worker1_queue'},
    'get_plancharge_data_mdb': {'queue': 'worker2_queue'},
    'get_ordo_data_mdb': {'queue': 'worker2_queue'},
    'get_last10OF_data_mdb': {'queue': 'worker2_queue'},
    'get_pdc_machine_data_mdb': {'queue': 'worker2_queue'},
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')