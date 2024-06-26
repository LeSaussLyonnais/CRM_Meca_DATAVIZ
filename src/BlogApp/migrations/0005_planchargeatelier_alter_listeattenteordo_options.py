# Generated by Django 5.0.2 on 2024-05-06 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0004_alter_listeattenteordo_date_debut_ordo'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanChargeAtelier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('COSECT', models.CharField(blank=True, default='ATXXX', max_length=10)),
                ('ANNEE', models.IntegerField(blank=True, default=0)),
                ('SEMAINE', models.IntegerField(blank=True, default=0)),
                ('COFRAIS', models.CharField(blank=True, default='XXX', max_length=50)),
                ('DESIGN', models.CharField(blank=True, default='MACHINE XXX', max_length=200)),
                ('VDUREE', models.FloatField(blank=True, default=0)),
            ],
            options={
                'ordering': ['COFRAIS'],
                'managed': True,
            },
        ),
        migrations.AlterModelOptions(
            name='listeattenteordo',
            options={'managed': True, 'ordering': ['DATE_DEBUT_ORDO']},
        ),
    ]
