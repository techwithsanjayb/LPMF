# Generated by Django 3.2.9 on 2022-07-21 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0009_auto_20220721_1034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userregistration',
            options={'ordering': ['userregistration_email_field'], 'verbose_name_plural': 'User Registration'},
        ),
    ]
