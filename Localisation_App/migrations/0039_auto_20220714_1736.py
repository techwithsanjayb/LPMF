# Generated by Django 3.2.9 on 2022-07-14 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0038_alter_translationquote_uer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translationquote',
            name='admin_remark',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='translationquote',
            name='client_remark',
            field=models.TextField(max_length=50, null=True),
        ),
    ]
