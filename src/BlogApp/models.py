import json

from django.db import models
from django.utils import timezone
from django_enum_choices.fields import EnumChoiceField
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.core.exceptions import ObjectDoesNotExist

from .enums import TimeInterval, SetupStatus


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


###########################################################################################################
####################################""Nouvelle BDD ########################################################
###########################################################################################################

class Site(models.Model):
    COSECT = models.CharField(max_length=10, default='ATXXX', blank=True, unique=True)
    Libelle_Site = models.CharField(max_length=50, default='Site XXX', blank=True)
    VAR_AFF_SITE = models.BooleanField(default=1)

    def __str__(self):
        return str(self.COSECT)

    class Meta:
        ordering = ['COSECT']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True


class Atelier(models.Model):
    Libelle_Atelier = models.CharField(max_length=50, default='XXX', blank=True) # , unique=True
    VAR_AFF_AT = models.BooleanField(default=1)
    # Libelle_Atelier = models.CharField(max_length=50, default='Atelier XXx', blank=True)
    At_Site_ID = models.ForeignKey(Site, on_delete=models.CASCADE, to_field='COSECT', default='DEFAULT')

    def __str__(self):
        return str(self.Libelle_Atelier)

    class Meta:
        ordering = ['Libelle_Atelier']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True


# def get_first_atelier():
#     try:
#         return Atelier.objects.order_by('id').first().id
#     except (Atelier.DoesNotExist, AttributeError):
#         # Créer un Atelier par défaut si aucun n'existe
#         default_atelier = Atelier.objects.create(Libelle_Atelier='XXX', VAR_AFF_AT=0)
#         return default_atelier.id

class Poste(models.Model):
    COFRAIS = models.CharField(max_length=10, default='XXX', blank=True, unique=True)
    DESIGN = models.CharField(max_length=50, default='Machine XXX', blank=True)
    VAR_AFF = models.BooleanField(default=1)
    Site_ID = models.ForeignKey(Site, on_delete=models.CASCADE, to_field='COSECT', default='DEFAULT')
    Atelier_ID = models.ForeignKey(Atelier, on_delete=models.CASCADE) # , to_field='INDICATEUR_DESIGN', default='XXx'

    def __str__(self):
        return str(self.COFRAIS)

    class Meta:
        ordering = ['COFRAIS']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True


class Ordre_Frabrication(models.Model):
    GACLEUNIK = models.CharField(max_length=50, default='XXX', blank=True) # , unique=True
    DATE_CHARGE = models.DateField(blank=True, null=True)
    DATE_ORDO = models.DateField(blank=True, null=True)
    HEURE_ORDO = models.TimeField(blank=True, null=True)
    DATEORDOOLD = models.DateTimeField(blank=True, null=True)
    CLIENT_NOM = models.CharField(max_length=50, default='XXX', blank=True, null=True)
    NAF = models.CharField(max_length=50, default='XXX', blank=True)
    ETATAF = models.CharField(max_length=10, default='X', blank=True)
    RANG = models.CharField(max_length=50, default='XXX', blank=True)
    EN_PIECE = models.CharField(max_length=100, default='XXX', blank=True)
    PHASE = models.IntegerField(default=0, blank=True)
    QTEAF = models.FloatField(default=0, blank=True)
    QTEAFREST = models.FloatField(default=0, blank=True)
    GA_PREP = models.FloatField(default=0, blank=True)
    GA_NBH = models.FloatField(default=0, blank=True)
    GA_NBHR = models.FloatField(default=0, blank=True)
    TYPEAF = models.CharField(max_length=2, default='XXX', blank=True)
    OPFINIE = models.CharField(max_length=2, default='X', blank=True)
    FLAG_URGENCE = models.BooleanField(default=0)
    OF_Poste_ID = models.ForeignKey(Poste, on_delete=models.CASCADE, to_field='COFRAIS', default='C35-2')

    def __str__(self):
        return str(self.GACLEUNIK)

    class Meta:
        ordering = ['GACLEUNIK']
        managed = True # Assurez-vous que cette ligne est soit absente, soit à True


class Charge(models.Model):
    VDUREE = models.FloatField(default=0, blank=True)
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

class Asso_Atelier_Info_Desc(models.Model):
    Atelier_ID = models.ForeignKey(Atelier, on_delete=models.CASCADE, to_field='id')
    Info_Des_ID = models.ForeignKey(Infos_Des, on_delete=models.CASCADE, to_field='id')



#Classes pour configurer le setup de django-celery-beat
class Setup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setups'

    title = models.CharField(max_length=70, blank=False)
    status = EnumChoiceField(SetupStatus, default=SetupStatus.active)
    created_at = models.DateTimeField(auto_now_add=True)
    time_interval = EnumChoiceField(
        TimeInterval, default=TimeInterval.five_secs)
    nom_site = models.CharField(max_length=70, default='ATCRM', blank=False)
    nom_atelier = models.CharField(max_length=70, default='XXX', blank=False)
    num_semaine = models.IntegerField(default=0, blank=True)
    num_annee = models.IntegerField(default=0, blank=True)
    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()

        return super(self.__class__, self).delete(*args, **kwargs)

    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            name=self.title,
            task='get_plancharge_data_mdb',
            interval=self.interval_schedule,
            args=json.dumps([self.id]),
            start_time=timezone.now()
        )
        self.save()

    @property
    def interval_schedule(self):
        if self.time_interval == TimeInterval.five_secs:
            return IntervalSchedule.objects.get(every=5, period='seconds')

        raise NotImplementedError(
            '''Interval Schedule for {interval} is not added.'''.format(
                interval=self.time_interval.value))


class Setup_OF(models.Model):
    class Meta:
        verbose_name = 'Setup_OF'
        verbose_name_plural = 'Setups_OF'

    title = models.CharField(max_length=70, blank=False)
    status = EnumChoiceField(SetupStatus, default=SetupStatus.active)
    created_at = models.DateTimeField(auto_now_add=True)
    time_interval = EnumChoiceField(
        TimeInterval, default=TimeInterval.five_secs)
    nom_poste = models.CharField(max_length=70, blank=False)
    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()

        return super(self.__class__, self).delete(*args, **kwargs)

    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            name=self.title,
            task='get_ordo_data_mdb',
            interval=self.interval_schedule,
            args=json.dumps([self.id]),
            start_time=timezone.now()
        )
        self.save()

    @property
    def interval_schedule(self):
        if self.time_interval == TimeInterval.five_secs:
            return IntervalSchedule.objects.get(every=5, period='seconds')

        raise NotImplementedError(
            '''Interval Schedule for {interval} is not added.'''.format(
                interval=self.time_interval.value))


class Setup_Last10OF(models.Model):
    class Meta:
        verbose_name = 'Setup_Last10OF'
        verbose_name_plural = 'Setups_Last10OF'

    title = models.CharField(max_length=70, blank=False)
    status = EnumChoiceField(SetupStatus, default=SetupStatus.active)
    created_at = models.DateTimeField(auto_now_add=True)
    time_interval = EnumChoiceField(
        TimeInterval, default=TimeInterval.five_secs)
    nom_poste = models.CharField(max_length=70, blank=False)
    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()

        return super(self.__class__, self).delete(*args, **kwargs)

    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            name=self.title,
            task='get_last10OF_data_mdb',
            interval=self.interval_schedule,
            args=json.dumps([self.id]),
            start_time=timezone.now()
        )
        self.save()

    @property
    def interval_schedule(self):
        if self.time_interval == TimeInterval.five_secs:
            return IntervalSchedule.objects.get(every=5, period='seconds')

        raise NotImplementedError(
            '''Interval Schedule for {interval} is not added.'''.format(
                interval=self.time_interval.value))


class Setup_PDCMachine(models.Model):
    class Meta:
        verbose_name = 'Setup_PDCMachine'
        verbose_name_plural = 'Setups_PDCMachine'

    title = models.CharField(max_length=70, blank=False)
    status = EnumChoiceField(SetupStatus, default=SetupStatus.active)
    created_at = models.DateTimeField(auto_now_add=True)
    time_interval = EnumChoiceField(
        TimeInterval, default=TimeInterval.five_secs)
    nom_poste = models.CharField(max_length=70, blank=False)
    num_semaine = models.IntegerField(default=0, blank=True)
    num_annee = models.IntegerField(default=0, blank=True)
    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()

        return super(self.__class__, self).delete(*args, **kwargs)

    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            name=self.title,
            task='get_pdc_machine_data_mdb',
            interval=self.interval_schedule,
            args=json.dumps([self.id]),
            start_time=timezone.now()
        )
        self.save()

    @property
    def interval_schedule(self):
        if self.time_interval == TimeInterval.five_secs:
            return IntervalSchedule.objects.get(every=5, period='seconds')

        raise NotImplementedError(
            '''Interval Schedule for {interval} is not added.'''.format(
                interval=self.time_interval.value))