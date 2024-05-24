from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.http import JsonResponse
from django.forms.models import model_to_dict
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
@api_view(['GET'])
def endpt_getsite(request):
    request_data = request.data

    sites = Site.objects.values(
        'COSECT',
        'Libelle_Site'
    )

    resultat = {
        'Sites': list(sites)
    }
    # print(resultat)

    return Response(resultat)


@api_view(['POST'])
def endpt_getatelier(request):
    request_data = request.data
    print(request_data)

    site = request_data.get('site', None)

    ateliers = Atelier.objects.filter(
        At_Site_ID__COSECT=site
    ).values(
        'Libelle_Atelier'
    )

    resultat = {
        'Ateliers': list(ateliers)
    }
    print(resultat)

    return Response(resultat)


@api_view(['POST'])
def endpt_popup_addatelier(request):
    # Récupérer les données de la requête
    request_data = request.data

    # Mettre à jour les variables si elles sont présentes dans la requête
    site = request_data.get('site', None)

    # Get the related Poste objects
    postes = Poste.objects.filter(
        Site_ID__COSECT=site,
        Atelier_ID__Libelle_Atelier = 'DEFAULT'
    ).values(
        'COFRAIS'
        # 'DESIGN'
    )

    resultat = {
        'Postes': list(postes)
    }
    # print(resultat)

    return Response(resultat)


@api_view(['POST'])
def endpt_addatelier(request):
    # Récupérer les données de la requête
    request_data = request.data

    # Mettre à jour les variables si elles sont présentes dans la requête
    site = request_data.get('site', None)
    atelier = request_data.get('atelier', None)
    postes = request_data.get('postes', None)

    # Vérifier que les données nécessaires sont présentes
    if not site or not atelier:
        return Response({'error': 'Site and atelier are required'}, status=400)

    try:
        # Créer ou récupérer l'atelier
        new_atelier, created = Atelier.objects.get_or_create(
            Libelle_Atelier=atelier,
            At_Site_ID__COSECT=site
        )

        # Récupérer l'ID de l'atelier
        # atelier_created = new_atelier.id

        # Si des postes sont fournis, les associer à l'atelier
        if postes:
            for poste in postes:
                poste_obj = get_object_or_404(Poste, COFRAIS=poste)

                # Mettre à jour les champs du poste
                poste_obj.Atelier_ID = new_atelier

                # Sauvegarder les modifications
                poste_obj.save()

        return Response({'atelier_id': new_atelier}, status=201)

    except Exception as e:
        return Response({'error': str(e)}, status=500)




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




@api_view(['POST'])
def endpoint_pdc(request):
    # Variables globales
    site = 'ATCRM'
    atelier = 'XXX'
    annee = '2024'

    # Récupérer les données de la requête
    request_data = request.data

    # Mettre à jour les variables si elles sont présentes dans la requête
    # site = request_data.get('site', site)
    # atelier = request_data.get('atelier', atelier)
    # annee = request_data.get('annee', annee)
    semaine = request_data.get('semaine', None)

    # Get the atelier object
    atelier_obj = get_object_or_404(Atelier, INDICATEUR_DESIGN=atelier)
    
    # Get the related Poste objects
    postes = Poste.objects.filter(Atelier_ID=atelier_obj).values('COFRAIS', 'DESIGN')
    
    # Get the charges related to these Poste objects
    charges = Charge.objects.filter(Poste_ID__in=postes.values('COFRAIS'), ANNEE=annee, SEMAINE=semaine).values('ANNEE', 'SEMAINE', 'VDUREE')

    resultat = {
        'Atelier_id': atelier_obj.INDICATEUR_DESIGN,
        'Poste_ids': list(postes),
        'Charge': list(charges)
    }
    # charges = list(resultats)

    return Response(resultat)