from django.urls import path, include
#from django.conf.urls import url
from .views import index, endpt_popup_addatelier, endpt_addatelier, TachePDCView

urlpatterns = [
    path('', index, name="blog-index"),
    path('PopupAjoutAtelier', endpt_popup_addatelier, name="page_popup_ajout_atelier"),
    path('AjoutAtelier', endpt_addatelier, name="page_ajout_atelier"),
    path('Site_<str:nom_site>/Atelier_<str:nom_atelier>/Annee_<str:num_annee>/Semaine_<str:num_semaine>/', TachePDCView.as_view(), name="blog-tache")
]