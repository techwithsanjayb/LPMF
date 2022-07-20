# Generated by Django 3.2.9 on 2022-07-20 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localisation_App', '0007_auto_20220719_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketingSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MarketingSection_lines', models.CharField(max_length=200)),
                ('MarketingSection_icon', models.ImageField(blank=True, null=True, upload_to='Localisation_App/Images')),
                ('MarketingSection_PublishedStatus', models.CharField(choices=[('Published', 'PUBLISHED'), ('Unpublished', 'UNPUBLISHED')], default='published', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'MarketingSection',
                'ordering': ['MarketingSection_lines'],
            },
        ),
    ]