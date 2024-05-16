from django.contrib import admin

# Register your models here.

from .models import *

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


"""
Credentials SuperUser : 
- Username : thoma
- Password : lapomme
"""