# Generated by Django 3.2.9 on 2022-07-14 20:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0006_alter_translationquote_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translationquote',
            name='submission_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 15, 1, 56, 25, 293808)),
        ),
    ]
