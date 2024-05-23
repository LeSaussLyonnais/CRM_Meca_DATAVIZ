from django.contrib import admin

# Register your models here.

<<<<<<< HEAD
from .models import Weather, ListeAttenteOrdo, PlanChargeAtelier, Site, Atelier, Poste, Charge, Absences, Accidents, Infos_Asc, Infos_Des, Setup
=======
from .models import *
>>>>>>> dev_front

admin.site.register(Weather)
admin.site.register(PlanChargeAtelier)
admin.site.register(Site)
admin.site.register(Atelier)
admin.site.register(Poste)
admin.site.register(Charge)
admin.site.register(Absences)
admin.site.register(Accidents)
admin.site.register(Infos_Asc)
admin.site.register(Infos_Des)
<<<<<<< HEAD

@admin.register(Setup)
class SetupAdmin(admin.ModelAdmin):
    list_display = [
        '__str__'
    ]
=======
>>>>>>> dev_front


"""
Credentials SuperUser : 
- Username : thoma
- Password : lapomme
"""