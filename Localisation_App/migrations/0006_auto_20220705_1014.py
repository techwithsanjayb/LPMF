# Generated by Django 3.2.9 on 2022-07-05 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0005_successstories_successstories_cdac_contribution'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='footermenuitems',
            options={'ordering': ['id'], 'verbose_name_plural': 'Footer Menu Items'},
        ),
        migrations.AlterModelOptions(
            name='topmenuitems',
            options={'ordering': ['id'], 'verbose_name_plural': 'Top Menu Items'},
        ),
        migrations.AddField(
            model_name='topmenuitems',
            name='Url_Path',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]