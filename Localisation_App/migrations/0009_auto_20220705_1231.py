# Generated by Django 3.2.9 on 2022-07-05 07:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0008_userregistration'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregistration',
            name='registration_User_Type',
            field=models.CharField(choices=[('Individual', 'Individual'), ('Organization', 'Organization'), ('DomainExpert', 'DomainExpert')], default='Individual', max_length=50),
        ),
        migrations.AlterField(
            model_name='userregistration',
            name='userregistration_phone_number',
            field=models.IntegerField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
