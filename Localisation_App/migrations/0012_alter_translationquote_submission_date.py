# Generated by Django 3.2.9 on 2022-07-14 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0011_alter_translationquote_submission_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translationquote',
            name='submission_date',
            field=models.DateField(null=True),
        ),
    ]