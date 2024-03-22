from django.urls import path

from .consumers import WeatherConsumer

websocket_urlpatterns = [
    path('ws/weather/', WeatherConsumer.as_asgi())
]