from rest_framework import serializers
from .models import Weather

# Definition de la classe qui permet de sérialiser les données à envoyer au react ou à intégrer en JSON
class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ['dt_txt', 'temp', 'icon']