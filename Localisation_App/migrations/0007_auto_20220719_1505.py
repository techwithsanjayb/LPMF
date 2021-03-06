# Generated by Django 3.2.9 on 2022-07-19 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0006_alter_translationquote_client_remark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translationquote',
            name='admin_remark',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='translationquote',
            name='status',
            field=models.CharField(blank=True, choices=[('PENDING', 'PENDING'), ('INPROCESS', 'INPROCESS'), ('COMPLETED', 'COMPLETED')], default='PENDING', max_length=50, null=True),
        ),
    ]
