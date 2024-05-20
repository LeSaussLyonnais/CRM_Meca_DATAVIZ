from django.shortcuts import render
from rest_framework.views import APIView
from .models import Weather, ListeAttenteOrdo, Setup
from .serializer import *
from rest_framework.response import Response
from .tasks import get_plancharge_data_mdb
from .enums import TimeInterval, SetupStatus

from django_celery_beat.models import PeriodicTask, IntervalSchedule
#from ProjetDjango1.celery import obtenir_valeur_de_x
import json
import requests
from django.http import HttpResponse
from django.views import View

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
    # Appeler la fonction pour obtenir la valeur de x
    global valeur_de_x
    # Incrémentez la valeur de x
    valeur_de_x += 1
    # Appelez la tâche planifiée en passant la valeur de x
    # get_plancharge_data_mdb.apply_async(args=(valeur_de_x,))
    # Répondez avec un message de confirmation ou toute autre réponse appropriée
    return HttpResponse("La tâche a été planifiée avec succès avec la valeur de x : {}".format(valeur_de_x))



def article(request, num_semaine):
    interval = IntervalSchedule.objects.get(every=10, period='seconds')
    task = PeriodicTask.objects.create(interval=interval, name=f"pdc_task_semaine_{num_semaine}", task='BlogApp.tasks.get_plancharge_data_mdb', args = json.dumps((num_semaine,)))
    #return render(request, f"BlogApp/article{num_semaine}.html")
    return HttpResponse(f"Tâche {num_semaine} créée")

class TachePDCView(View):
    def dispatch(self, request, *args, **kwargs):
        # Créer la tâche périodique uniquement lorsque l'utilisateur accède à la vue
        self.num_semaine = kwargs.get('num_semaine')
        self.num_annee = kwargs.get('num_annee')
        self.nom_atelier = kwargs.get('nom_atelier')
        self.nom_site = kwargs.get('nom_site')
        self.interval = TimeInterval.five_secs
        self.title = f"Setup_{self.nom_site}_{self.nom_atelier}_{self.num_annee}_{self.num_semaine}"
        self.setup_pdc = Setup.objects.create(
            title=self.title, 
            time_interval=self.interval, 
            nom_site=self.nom_site, 
            nom_atelier=self.nom_atelier, 
            num_annee=self.num_annee, 
            num_semaine=self.num_semaine
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