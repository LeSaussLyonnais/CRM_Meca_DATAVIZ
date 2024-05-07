# Generated by Django 5.0.2 on 2024-04-11 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListeAttenteOrdo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NUM_AFFAIRE', models.IntegerField(blank=True, default=0)),
                ('DATE_DEBUT_ORDO', models.IntegerField(blank=True, default=0)),
                ('CLIENT', models.CharField(blank=True, default='ICAM', max_length=200)),
                ('ETAT_AFFAIRE', models.CharField(blank=True, default='X', max_length=50)),
                ('RANG_OF', models.CharField(blank=True, default='X', max_length=50)),
                ('TEMPS_PREVU', models.IntegerField(blank=True, default=0)),
                ('TEMPS_ECOULE', models.IntegerField(blank=True, default=0)),
                ('TEMPS_RESTANT', models.IntegerField(blank=True, default=0)),
            ],
        ),
    ]