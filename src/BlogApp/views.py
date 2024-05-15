from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse



import requests
#from django.http import HttpResponse

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

def charge(request):
    return render(request, "BlogApp/PlanCharge.html")

def ordo(request):

    liste_ordo = ListeAttenteOrdo.objects.all()

    return render(request, "BlogApp/test_data_liste_ordo.html", context={'liste_ordo': liste_ordo})

def article(request, num_article):
    return render(request, f"BlogApp/article{num_article}.html")

#Vues React
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
    atelier = 'TOUR'
    annee = '2024'
    semaine = '13'

        # Récupérer les données de la requête
    request_data = request.data

    # Mettre à jour les variables si elles sont présentes dans la requête
    # site = request_data.get('site', site)
    # atelier = request_data.get('atelier', atelier)
    # annee = request_data.get('annee', annee)
    semaine = request_data.get('semaine', semaine)

    resultats = PlanChargeAtelier.objects.filter(COSECT__startswith=site, ANNEE=annee, SEMAINE=semaine, DESIGN__icontains=atelier).values('COSECT', 'ANNEE', 'SEMAINE', 'COFRAIS', 'DESIGN', 'VDUREE')

    charges = list(resultats)

    return Response(resultats)