from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Q
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.utils.crypto import get_random_string

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import *
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

# @api_view(['POST'])
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


class TacheListeOrdoView(View):
    def dispatch(self, request, *args, **kwargs):
        # Créer la tâche périodique uniquement lorsque l'utilisateur accède à la vue
        self.nom_poste = kwargs.get('nom_poste')
        self.interval = TimeInterval.five_secs
        self.title = f"Setup_OF_{self.nom_poste}"
        # Utiliser get_or_create pour éviter de dupliquer l'objet
        self.setup_OF, created = Setup_OF.objects.get_or_create(
            title=self.title, 
            defaults={
                'time_interval': self.interval,
                'nom_poste': self.nom_poste
            }
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(
            request, 'BlogApp/ListeOrdo.html',
            context={
                'nom_poste': self.nom_poste
            }
        )


class TacheLast10OFView(View):
    def dispatch(self, request, *args, **kwargs):
        # Créer la tâche périodique uniquement lorsque l'utilisateur accède à la vue
        self.nom_poste = kwargs.get('nom_poste')
        self.interval = TimeInterval.five_secs
        self.title = f"Setup_Last10OF_{self.nom_poste}"
        # Utiliser get_or_create pour éviter de dupliquer l'objet
        self.setup_last10OF, created = Setup_Last10OF.objects.get_or_create(
            title=self.title, 
            defaults={
                'time_interval': self.interval,
                'nom_poste': self.nom_poste
            }
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(
            request, 'BlogApp/Last10OF.html',
            context={
                'nom_poste': self.nom_poste
            }
        )


class TachePDCMachineView(View):
    def dispatch(self, request, *args, **kwargs):
        # Créer la tâche périodique uniquement lorsque l'utilisateur accède à la vue
        self.num_semaine = kwargs.get('num_semaine')
        self.num_annee = kwargs.get('num_annee')
        self.nom_poste = kwargs.get('nom_poste')
        self.interval = TimeInterval.five_secs
        self.title = f"Setup_PDCMachine_{self.nom_poste}_{self.num_annee}_{self.num_semaine}"
        # Utiliser get_or_create pour éviter de dupliquer l'objet
        self.setup_pdc_machine, created = Setup_PDCMachine.objects.get_or_create(
            title=self.title, 
            defaults={
                'time_interval': self.interval,
                'nom_poste': self.nom_poste,
                'num_annee': self.num_annee, 
                'num_semaine': self.num_semaine
            }
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(
            request, 'BlogApp/PDCMachine.html',
            context={
                'nom_poste': self.nom_poste,
                'num_annee': self.num_annee, 
                'num_semaine': self.num_semaine
            }
        )

################################################################################################
###################################### Section Vues REACT ######################################
################################################################################################

# def get_or_create_user_session_id(request):
#     if 'user_session_id' not in request.session:
#         request.session['user_session_id'] = get_random_string(32)
#     return request.session['user_session_id']


@api_view(['POST'])
def endpt_pdc_tache(request):
    """
    Fonction pour générer la tâche get ordo data mdb
    """
    request_data = request.data

    num_semaine = request_data.get('num_semaine')
    num_annee = request_data.get('num_annee')
    nom_atelier = request_data.get('nom_atelier')
    nom_site = request_data.get('nom_site')
    num_current_semaine = request_data.get('num_current_semaine')
    
    # num_setup = num_semaine - num_current_semaine
    
    interval = TimeInterval.five_secs
    # user_session_id = get_or_create_user_session_id(request)
    title = f"Setup_{nom_site}_{nom_atelier}_{num_annee}_{num_semaine}"

    setup_pdc, created = Setup.objects.get_or_create(
        title=title, 
        defaults={
            'time_interval': interval,
            'nom_site': nom_site, 
            'nom_atelier': nom_atelier, 
            'num_annee': num_annee, 
            'num_semaine': num_semaine,
            # 'num_current_semaine': num_current_semaine,
        }
    )
    
    try:
        setup_pdc_too_old = Setup.objects.get(
            num_semaine__lt=num_current_semaine,
        )
        setup_pdc_too_old.delete()
    except Setup.DoesNotExist:
        pass

    return Response({'PDC_Semaine': "PDC Semaine "+str(num_semaine)+" generated"}, status=201)


@api_view(['POST'])
def endpt_ordo_getposte(request):
    request_data = request.data

    atelier = request_data.get('atelier', None)

    postes = Poste.objects.filter(
        Atelier_ID__Libelle_Atelier = atelier
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
def endpt_ordo_tache(request):
    request_data = request.data

    nom_poste = request_data.get('nom_poste')
    if not nom_poste:
        return Response({'error': 'nom_poste is required'}, status=400)

    interval = TimeInterval.five_secs
    title = f"Setup_OF_{nom_poste}"

    setup_OF, created = Setup_OF.objects.get_or_create(
        title=title, 
        defaults={
            'time_interval': interval,
            'nom_poste': nom_poste
        }
    )

    return Response({'Ordo_Poste': f"Ordo Poste {nom_poste} generated"}, status=201)


@api_view(['POST'])
def endpt_last10of_tache(request):
    request_data = request.data

    nom_poste = request_data.get('nom_poste')
    if not nom_poste:
        return Response({'error': 'nom_poste is required'}, status=400)

    interval = TimeInterval.five_secs
    title = f"Setup_Last10OF_{nom_poste}"

    setup_last10of, created = Setup_Last10OF.objects.get_or_create(
        title=title, 
        defaults={
            'time_interval': interval,
            'nom_poste': nom_poste
        }
    )

    return Response({'Last10OF_Poste': f"Last 10 OF Poste {nom_poste} generated"}, status=201)


@api_view(['POST'])
def endpt_pdc_machine_tache(request):
    request_data = request.data

    num_semaine = request_data.get('num_semaine')
    num_annee = request_data.get('num_annee')
    nom_poste = request_data.get('nom_poste')
    if not nom_poste:
        return Response({'error': 'nom_poste is required'}, status=400)

    interval = TimeInterval.five_secs
    title = f"Setup_PDCMachine_{nom_poste}_{num_annee}_{num_semaine}"

    setup_pdc_machine, created = Setup_PDCMachine.objects.get_or_create(
        title=title, 
        defaults={
            'time_interval': interval,
            'nom_poste': nom_poste,
            'num_annee': num_annee, 
            'num_semaine': num_semaine
        }
    )

    try:
        setup_pdc_machine_too_old = Setup_PDCMachine.objects.get(
            num_semaine__lt=num_semaine,
        )
        setup_pdc_machine_too_old.delete()
    except Setup_PDCMachine.DoesNotExist:
        pass

    return Response({'PDC_Machine': f"PDC Machine {nom_poste} generated"}, status=201)     


#Vues React
@api_view(['GET'])
def endpt_getsite(request):
    request_data = request.data

    sites = Site.objects.filter(
        ~Q(Libelle_Site='Site XXX'), Q(Libelle_Site='Site XXX') | ~Q(Libelle_Site='Site XXX'), ~Q(Libelle_Site='Site XXX')
    ).values(
        'COSECT',
        'Libelle_Site'
    )

    resultat = {
        'Sites': list(sites)
    }
    print(resultat)

    return Response(resultat)


@api_view(['POST'])
def endpt_getatelier(request):
    request_data = request.data

    site = request_data.get('site', None)

    ateliers = Atelier.objects.filter(
        At_Site_ID__COSECT=site,
        VAR_AFF_AT=1
    ).values(
        'Libelle_Atelier'
    )

    resultat = {
        'Ateliers': list(ateliers)
    }

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
        # Récupérer l'instance du site correspondant au COSECT fourni
        site_instance = get_object_or_404(Site, COSECT=site)
        
        # Créer ou récupérer l'atelier
        new_atelier, created = Atelier.objects.get_or_create(
            Libelle_Atelier=atelier,
            At_Site_ID=site_instance
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

        return Response({'atelier_id': new_atelier.Libelle_Atelier}, status=201)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['DELETE'])
def endpt_delatelier(request):
    # Récupérer les données de la requête
    request_data = request.data

    # Mettre à jour les variables si elles sont présentes dans la requête
    site = request_data.get('site', None)
    atelier = request_data.get('atelier', None)

    # Vérifier que les données nécessaires sont présentes
    if not site or not atelier:
        return Response({'error': 'Site and atelier are required'}, status=400)

    try:
        atelier_default = Atelier.objects.get(
            Libelle_Atelier='DEFAULT'
        )
        
        postes = Poste.objects.filter(
            Atelier_ID__Libelle_Atelier=atelier
        ).values_list(
            'COFRAIS',
            flat=True
        )

        for poste in postes:
            poste_obj = get_object_or_404(Poste, COFRAIS=poste)

            # Mettre à jour les champs du poste
            poste_obj.Atelier_ID = atelier_default

            # Sauvegarder les modifications
            poste_obj.save()

        # Récupérer et supprimer l'atelier
        atelier_del = Atelier.objects.get(
            Libelle_Atelier=atelier,
            At_Site_ID__COSECT=site
        )
        atelier_del.delete()
        return Response({'message': 'atelier supprimé'}, status=204)
    # except Atelier.DoesNotExist:
    #     return Response({'error_atelier_del': f"Setup {atelier_del.Libelle_Atelier} non trouvé"}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


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