from django.urls import path, include
#from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', index, name="blog-index"),
    path('AjoutAtelier', endpt_addatelier, name="page_accueil_ajout_atelier"),
    path('DeleteAtelier', endpt_delatelier, name="page_accueil_delete_atelier"),
    path('getSite', endpt_getsite, name="page_accueil_upload_sites"),
    path('getAtelier', endpt_getatelier, name="page_accueil_upload_ateliers"),
    path('PopupAjoutAtelier', endpt_popup_addatelier, name="page_accueil_popup_ajout_atelier"),
    path('PDC_Atelier_Tache', endpt_pdc_tache, name="page_PDC_Atelier_TacheWS"),
    path('Ordo_getPoste', endpt_ordo_getposte, name="page_ordo_Atelier"),
    path('Ordo_Poste_Tache', endpt_ordo_tache, name="page_Ordo_Poste_TacheWS"),
    path('Site_<str:nom_site>/Atelier_<str:nom_atelier>/Annee_<str:num_annee>/Semaine_<str:num_semaine>/', TachePDCView.as_view(), name="blog-tache"),
    path('Ordo_Poste_<str:nom_poste>/', TacheListeOrdoView.as_view(), name="blog-tache-Ordo")
]