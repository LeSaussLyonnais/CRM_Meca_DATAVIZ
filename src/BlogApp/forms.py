from django import forms
from .models import ListeAttenteOrdo

class ListeAttenteOrdoForm(forms.ModelForm):
    class Meta:
        model = ListeAttenteOrdo
        fields = "__all__"