from django.contrib import admin

# Register your models here.

from .models import Weather, ListeAttenteOrdo, PlanChargeAtelier

admin.site.register(Weather)
admin.site.register(PlanChargeAtelier)


"""
Credentials SuperUser : 
- Username : thoma
- Password : lapomme
"""