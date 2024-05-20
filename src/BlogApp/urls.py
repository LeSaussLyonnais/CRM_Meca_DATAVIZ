from django.urls import path, include
#from django.conf.urls import url
from .views import index, ordo, article, WeatherView, charge, TachePDCView

urlpatterns = [
    path('', index, name="blog-index"),
    path('ordo/', ordo, name="blog-ordo"),
    path('charge/', charge, name="charge"),
    path('article<str:num_article>/', article, name="blog-article"),
    path('Site_<str:nom_site>/Atelier_<str:nom_atelier>/Annee_<str:num_annee>/Semaine_<str:num_semaine>/', TachePDCView.as_view(), name="blog-tache")
]