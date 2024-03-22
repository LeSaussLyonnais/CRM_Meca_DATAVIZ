# Pour lancer Celery automatiquement lorsque django se lance
from .celery import app as celery_app

__all__ = ['celery_app']