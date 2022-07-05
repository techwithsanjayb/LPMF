# Generated by Django 3.2.9 on 2022-07-05 05:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0007_remove_topmenuitems_url_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('userregistration_user_id', models.AutoField(primary_key=True, serialize=False)),
                ('userregistration_first_name', models.CharField(max_length=60)),
                ('userregistration_middle_name', models.CharField(max_length=60)),
                ('userregistration_last_name', models.CharField(max_length=60)),
                ('userregistration_email_field', models.EmailField(max_length=60, unique=True)),
                ('userregistration_phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('userregistration_password', models.CharField(max_length=30)),
                ('userregistration_confirm_password', models.CharField(max_length=30)),
                ('userregistration_active_status', models.BooleanField(default=False)),
                ('userregistration_registration_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'User Registration',
            },
        ),
    ]