# Generated by Django 3.2.9 on 2022-07-14 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0033_alter_resourcedata_resourcedata_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolsdata',
            name='ToolsData_slug',
            field=models.SlugField(blank=True, max_length=2000, null=True),
        ),
    ]