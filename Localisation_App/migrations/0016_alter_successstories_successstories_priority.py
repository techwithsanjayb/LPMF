# Generated by Django 3.2.9 on 2022-07-07 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0015_successstories_successstories_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='successstories',
            name='SuccessStories_Priority',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], max_length=10, null=True),
        ),
    ]