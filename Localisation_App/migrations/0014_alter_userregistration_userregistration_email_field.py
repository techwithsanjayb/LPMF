# Generated by Django 3.2.9 on 2022-07-06 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0013_alter_userregistration_userregistration_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistration',
            name='userregistration_email_field',
            field=models.EmailField(max_length=60),
        ),
    ]