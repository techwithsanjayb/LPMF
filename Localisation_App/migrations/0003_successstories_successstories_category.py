# Generated by Django 3.2.9 on 2022-07-04 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0002_remove_successstories_successstories_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='successstories',
            name='SuccessStories_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Localisation_App.successstories_category'),
        ),
    ]
