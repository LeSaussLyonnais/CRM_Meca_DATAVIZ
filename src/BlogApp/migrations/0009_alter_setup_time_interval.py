# Generated by Django 5.0.2 on 2024-05-19 09:28

import BlogApp.enums
import django_enum_choices.choice_builders
import django_enum_choices.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0008_setup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setup',
            name='time_interval',
            field=django_enum_choices.fields.EnumChoiceField(choice_builder=django_enum_choices.choice_builders.value_value, choices=[('5 secs', '5 secs'), ('10 secs', '10 secs'), ('30 secs', '30 secs'), ('1 min', '1 min'), ('5 mins', '5 mins'), ('1 hour', '1 hour')], default=BlogApp.enums.TimeInterval['five_mins'], enum_class=BlogApp.enums.TimeInterval, max_length=7),
        ),
    ]
