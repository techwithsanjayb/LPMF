# Generated by Django 3.2.9 on 2022-07-11 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0021_alter_translationquote_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='successstories',
            name='SuccessStories_PublishedStatus',
            field=models.CharField(choices=[('Published', 'PUBLISHED'), ('Unpublished', 'UNPUBLISHED')], default='published', max_length=20),
        ),
    ]
