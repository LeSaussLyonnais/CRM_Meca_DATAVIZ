from django.db import models

# Create your models here.
class Weather(models.Model):
    
    #wthr = models.CharField(max_length=50)
    dt_txt = models.CharField(max_length=50, blank=True, default='default_value')
    temp = models.FloatField(default=0, blank=True)
    icon = models.CharField(max_length=50, blank=True, default='default_value')
    #dt = models.IntegerField(default=0, blank=True)
    #symbol = models.CharField(max_length=50)
    #visibility = models.FloatField(default=0, blank=True)
    #rank = models.IntegerField(default=0, blank=True)
    #id = models.IntegerField(default=0, blank=True)
    #image = models.URLField(blank=True, null=True)
    
    
    def __str__(self):
        return str(self.dt_txt)
    
    
    class Meta:
        ordering = ['dt_txt']
        managed = True  # Assurez-vous que cette ligne est soit absente, soit à True


class ListeAttenteOrdo(models.Model):
    NUM_AFFAIRE = models.IntegerField(default=0, blank=True)
    DATE_DEBUT_ORDO = models.CharField(max_length=50, default=0, blank=True)
    CLIENT = models.CharField(max_length=200, blank=True, default='ICAM')
    ETAT_AFFAIRE = models.CharField(max_length=50, blank=True, default='X')
    RANG_OF = models.CharField(max_length=50, blank=True, default='X')
    TEMPS_PREVU = models.CharField(max_length=50, default=0, blank=True)
    TEMPS_ECOULE = models.CharField(max_length=50, default=0, blank=True)
    TEMPS_RESTANT = models.CharField(max_length=50, default=0, blank=True)

    def __str__(self):
        return str(self.NUM_AFFAIRE)

    class Meta:
        ordering = ['DATE_DEBUT_ORDO']
        managed = True  # Assurez-vous que cette ligne est soit absente, soit à True    


class PlanChargeAtelier(models.Model):
    COSECT = models.CharField(max_length=10, default='ATXXX', blank=True)
    ANNEE = models.IntegerField(default=0, blank=True)
    SEMAINE = models.IntegerField(default=0, blank=True)
    COFRAIS = models.CharField(max_length=50, default='XXX', blank=True)
    DESIGN = models.CharField(max_length=200, default='MACHINE XXX', blank=True)
    VDUREE = models.FloatField(default=0, blank=True)

    def __str__(self):
        return str(self.COFRAIS)

    class Meta:
        ordering = ['COFRAIS']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True