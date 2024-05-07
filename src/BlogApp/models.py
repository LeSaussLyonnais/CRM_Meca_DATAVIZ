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

    

