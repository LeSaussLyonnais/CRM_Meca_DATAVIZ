# Generated by Django 5.0.2 on 2024-06-20 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0002_setup_pdcmachine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordre_frabrication',
            name='DATE_CHARGE',
        ),
    ]
