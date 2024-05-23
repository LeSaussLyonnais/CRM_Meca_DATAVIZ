from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.http import JsonResponse
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Weather, ListeAttenteOrdo, Setup, Atelier, Poste, Site
from .serializer import *
from .tasks import get_plancharge_data_mdb
from .enums import TimeInterval, SetupStatus

import requests
import json


# Create your views here.
def index(request):
    '''
    url = 'https://api.openweathermap.org/data/2.5/forecast?lat=43.60&lon=1.433333&appid=86a1d03a37f156f8b34f6be197056295&units=metric'
    #url = 'https://api.openweathermap.org/data/2.5/weather?lat=43.60&lon=1.433333&appid=86a1d03a37f156f8b34f6be197056295'
    # Faut que je prenne une API qui me donne une liste de résultats pas juste les donnée d'un lieu à un seul instant
    data = requests.get(url).json()
    weather = data['list']
    '''
    '''
    url = 'https://coinlib.io/api/v1/coinlist?key=8dd1a71f03f492d3&pref=USD&page=1&order=rank_asc'
    data = requests.get(url).json()
    coins = data['coins']
    '''
    #print(response.json())
    return render(request, "BlogApp/index.html") # ", context={'weather': weather}"

class TachePDCView(View):
    def dispatch(self, request, *args, **kwargs):
        # Créer la tâche périodique uniquement lorsque l'utilisateur accède à la vue
        self.num_semaine = kwargs.get('num_semaine')
        self.num_annee = kwargs.get('num_annee')
        self.nom_atelier = kwargs.get('nom_atelier')
        self.nom_site = kwargs.get('nom_site')
        self.interval = TimeInterval.five_secs
        self.title = f"Setup_{self.nom_site}_{self.nom_atelier}_{self.num_annee}_{self.num_semaine}"
        # Utiliser get_or_create pour éviter de dupliquer l'objet
        self.setup_pdc, created = Setup.objects.get_or_create(
            title=self.title, 
            defaults={
                'time_interval': self.interval,
                'nom_site': self.nom_site, 
                'nom_atelier': self.nom_atelier, 
                'num_annee': self.num_annee, 
                'num_semaine': self.num_semaine
            }
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(
            request, 'BlogApp/PlanCharge.html',
            context={
                'nom_site': self.nom_site,
                'nom_atelier': self.nom_atelier,
                'num_annee': self.num_annee, 
                'num_semaine': self.num_semaine
            }
        )

    def delete(self, request, *args, **kwargs):
        # Supprimer la tâche périodique lorsque l'utilisateur quitte la vue
        try:
            setup_pdc = Setup.objects.get(title=self.title)
            setup_pdc.delete()
            return HttpResponse(f"Setup {self.num_semaine} supprimée")
        except PeriodicTask.DoesNotExist:
            return HttpResponse(f"Setup {self.num_semaine} non trouvée", status=404)


#Vues React



@api_view(['POST'])
def endpt_popup_addatelier(request):
    # Récupérer les données de la requête
    request_data = request.data

    # Mettre à jour les variables si elles sont présentes dans la requête
    site = request_data.get('site', None)

    # Get the related Poste objects
    postes = Poste.objects.filter(
        Site_ID__COSECT=site
    ).values(
        'COFRAIS',
        'DESIGN'
    )

    resultat = {
        'Postes': list(postes)
    }


@api_view(['POST'])
def endpt_addatelier(request):
    # Récupérer les données de la requête
    request_data = request.data

    # Mettre à jour les variables si elles sont présentes dans la requête
    site = request_data.get('site', None)
    atelier = request_data.get('atelier', None)
    postes = request_data.get['postes']

    new_atelier = Atelier.objects.create(
        Libelle_Atelier=atelier,
        At_Site_ID=site
    )

    for poste in postes:
        poste_obj = get_object_or_404(Poste, COFRAIS=poste['cofrais'])

        # Mettre à jour les champs du poste
        poste_obj.Atelier_ID = atelier

        # Sauvegarder les modifications
        poste_obj.save()



class WeatherView(APIView):
    def get(self, request):
        '''
        output = [{"dt_txt": output.dt_txt,
                    "temp": output.temp,
                    "icon": output.icon}
                    for output in Weather.objects.all()]
        '''
        output = Weather.objects.all()
        serializer = WeatherSerializer(output, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WeatherSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)