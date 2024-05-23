from django.urls import path, include
#from django.conf.urls import url
<<<<<<< HEAD
from .views import index, endpt_popup_addatelier, endpt_addatelier, TachePDCView

urlpatterns = [
    path('', index, name="blog-index"),
    path('PopupAjoutAtelier', endpt_popup_addatelier, name="page_popup_ajout_atelier"),
    path('AjoutAtelier', endpt_addatelier, name="page_ajout_atelier"),
    path('Site_<str:nom_site>/Atelier_<str:nom_atelier>/Annee_<str:num_annee>/Semaine_<str:num_semaine>/', TachePDCView.as_view(), name="blog-tache")
=======
from .views import *

urlpatterns = [
    path('', index, name="blog-index"),
    path('ordo', ordo, name="blog-ordo"),
    path('charge/', charge, name="charge"),
    path('chargeUpdate/', endpoint_pdc, name="chargeUpdate"),
    path('article<str:num_article>/', article, name="blog-article"),
    path('React', WeatherView.as_view(), name="WeatherReactView")
>>>>>>> dev_front
]