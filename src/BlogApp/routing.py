from django.urls import path

from .consumers import *

# Définition des chemins d'url qui constituent les channels où on envoi les messages en temps réel dès qu'il y a une modif 
websocket_urlpatterns = [
    path('ws/charge/<str:nom_site>/<str:nom_atelier>/<str:num_annee>/<str:num_semaine>/', PlanChargeConsumer.as_asgi()),
    path('ws/ordo/<str:nom_poste>/', ListeOrdoConsumer.as_asgi()),
    path('ws/last10of/<str:nom_poste>/', Last10OFConsumer.as_asgi()),
]

