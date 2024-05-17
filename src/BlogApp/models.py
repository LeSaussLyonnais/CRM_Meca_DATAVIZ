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


###############################################################################################################
####################################""Nouvelle BDD ########################################################

class Site(models.Model):
    COSECT = models.CharField(max_length=10, default='ATXXX', blank=True, unique=True)
    Libelle_Site = models.CharField(max_length=50, default='Site XXX', blank=True)

    def __str__(self):
        return str(self.COSECT)

    class Meta:
        ordering = ['COSECT']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True


class Atelier(models.Model):
    INDICATEUR_DESIGN = models.CharField(max_length=50, default='XXX', blank=True, unique=True)
    Libelle_Atelier = models.CharField(max_length=50, default='Atelier XXX', blank=True)

    def __str__(self):
        return str(self.INDICATEUR_DESIGN)

    class Meta:
        ordering = ['INDICATEUR_DESIGN']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True


class Poste(models.Model):
    COFRAIS = models.CharField(max_length=10, default='XXX', blank=True, unique=True)
    DESIGN = models.CharField(max_length=50, default='Machine XXX', blank=True)
    VAR_AFF = models.BooleanField(default=1)
    Site_ID = models.ForeignKey(Site, on_delete=models.CASCADE, to_field='COSECT')
    Atelier_ID = models.ForeignKey(Atelier, on_delete=models.CASCADE, to_field='INDICATEUR_DESIGN', default='XXX')

    def __str__(self):
        return str(self.COFRAIS)

    class Meta:
        ordering = ['COFRAIS']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True


class Ordres_Frabrication(models.Model):
    Ref_OF = models.CharField(max_length=50, default='XXX', blank=True, unique=True)
    Nom_Piece = models.CharField(max_length=50, default='Piece XXX', blank=True)
    Temps_Prevu = models.DecimalField(max_digits=15, decimal_places=6, default=0, blank=True)
    Date_Debut = models.DateTimeField(blank=True)
    Phase_OF = models.IntegerField(default=0, blank=True)
    Rang_OF = models.CharField(max_length=50, default='X', blank=True)

    def __str__(self):
        return str(self.Ref_OF)

    class Meta:
        ordering = ['Ref_OF']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True


class Charge(models.Model):
    VDUREE = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    ANNEE = models.IntegerField(default=0, blank=True)
    SEMAINE = models.IntegerField(default=0, blank=True)
    Poste_ID = models.ForeignKey(Poste, on_delete=models.CASCADE, to_field='COFRAIS')

    def __str__(self):
        return str(self.VDUREE)

    class Meta:
        ordering = ['VDUREE']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True


class Absences(models.Model):
    Libelle_Absence = models.CharField(max_length=50, default='Abs', blank=True)
    Type_Absence = models.CharField(max_length=50, default='None', blank=True)
    Commentaire_Absence = models.CharField(max_length=200, default='None', blank=True)
    Atelier_ID = models.ForeignKey(Atelier, on_delete=models.CASCADE, to_field='id')

    def __str__(self):
        return str(self.Libelle_Absence)

    class Meta:
        ordering = ['Libelle_Absence']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True


class Accidents(models.Model):
    Libelle_Accident = models.CharField(max_length=50, default='Acc', blank=True)
    Description_Accident = models.CharField(max_length=200, default='None', blank=True)
    Site_ID = models.ForeignKey(Site, on_delete=models.CASCADE, to_field='id')

    def __str__(self):
        return str(self.Libelle_Accident)

    class Meta:
        ordering = ['Libelle_Accident']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True


class Infos_Asc(models.Model):
    Libelle_Info_Asc = models.CharField(max_length=50, default='Info', blank=True)
    Descritpion_Info_Asc = models.CharField(max_length=200, default='None', blank=True)
    Destinataire = models.CharField(max_length=50, default='None', blank=True)
    Atelier_ID = models.ForeignKey(Atelier, on_delete=models.CASCADE, to_field='id')

    def __str__(self):
        return str(self.Libelle_Info_Asc)

    class Meta:
        ordering = ['Libelle_Info_Asc']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True


class Infos_Des(models.Model):
    Libelle_Info_Des = models.CharField(max_length=50, default='Com', blank=True)
    Descritpion_Info_Des = models.CharField(max_length=200, default='None', blank=True)

    def __str__(self):
        return str(self.Libelle_Info_Des)

    class Meta:
        ordering = ['Libelle_Info_Des']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True


class Asso_Postes_OF(models.Model):
    Poste_ID = models.ForeignKey(Poste, on_delete=models.CASCADE, to_field='COFRAIS')
    OF_ID = models.ForeignKey(Ordres_Frabrication, on_delete=models.CASCADE, to_field='Ref_OF')

class Asso_Atelier_Info_Desc(models.Model):
    Atelier_ID = models.ForeignKey(Atelier, on_delete=models.CASCADE, to_field='id')
    Info_Des_ID = models.ForeignKey(Infos_Des, on_delete=models.CASCADE, to_field='id')