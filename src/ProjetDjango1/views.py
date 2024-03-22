from django.shortcuts import render
from datetime import datetime
from BlogApp.tasks import get_weather_data

def index(request):
    date = datetime.today()
    #return(date)
    return render(request, "ProjetDjango1/index.html", context={"prenom": "Thomas", "jour": "lundi", "date": date})