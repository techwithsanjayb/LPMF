# Generated by Django 3.2.9 on 2022-07-14 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0034_toolsdata_toolsdata_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolsdata',
            name='ToolsData_slug',
            field=models.SlugField(blank=True, max_length=5000, null=True),
        ),
    ]
