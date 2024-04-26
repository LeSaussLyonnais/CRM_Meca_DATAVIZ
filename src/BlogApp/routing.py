from django.urls import path

from .consumers import WeatherConsumer, PlanChargeConsumer

# Définition des chemins d'url qui constituent les channels où on envoi les messages en temps réel dès qu'il y a une modif 
websocket_urlpatterns = [
    path('ws/weather/', WeatherConsumer.as_asgi()),
    path('ws/charge/', PlanChargeConsumer.as_asgi())
]

