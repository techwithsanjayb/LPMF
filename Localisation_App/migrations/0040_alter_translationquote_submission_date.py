# Generated by Django 3.2.9 on 2022-07-14 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0039_auto_20220714_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translationquote',
            name='submission_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
