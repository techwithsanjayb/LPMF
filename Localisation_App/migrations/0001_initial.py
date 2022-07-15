# Generated by Django 3.2.9 on 2022-07-14 19:39

import ckeditor.fields
import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('sub_title', models.CharField(max_length=100)),
                ('caption', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Carousel Data',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=10)),
                ('option', models.CharField(max_length=30)),
                ('comment', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Contact Us',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='EmpanelledAgencies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('contact_person', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Empanelled Agencies',
                'ordering': ['company_name'],
            },
        ),
        migrations.CreateModel(
            name='FAQs_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FAQs_CategoryType', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'FAQs Category',
                'ordering': ['FAQs_CategoryType'],
            },
        ),
        migrations.CreateModel(
            name='Footer_Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Footer_Links_Title', models.CharField(max_length=100)),
                ('Footer_Links_Content', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name_plural': 'Footer Links',
                'ordering': ['Footer_Links_Title'],
            },
        ),
        migrations.CreateModel(
            name='FooterMenuItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FooterMenuItems_Name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Footer Menu Items',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='GuidelinceForIndianGovWebsite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('percentage', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Guidelince For Indian Gov Website',
            },
        ),
        migrations.CreateModel(
            name='NewsAndEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NewsAndEvents_HeadingName', models.CharField(max_length=100)),
                ('NewsAndEvents_Discription', models.CharField(max_length=5000, null=True)),
                ('NewsAndEvents_CreationDate', models.DateTimeField(auto_now=True)),
                ('NewsAndEvents_UpdatedDate', models.DateTimeField(auto_now_add=True)),
                ('NewsAndEvents_Link', models.URLField()),
            ],
            options={
                'verbose_name_plural': 'News And Events',
                'ordering': ['NewsAndEvents_HeadingName'],
            },
        ),
        migrations.CreateModel(
            name='Resources_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Resources_CategoryType', models.CharField(max_length=100)),
                ('Resources_Cat_Status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Resources Category',
                'ordering': ['Resources_CategoryType'],
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Services_Name', models.CharField(max_length=100)),
                ('Services_Description', models.CharField(max_length=300)),
                ('Services_links', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name_plural': 'Services',
                'ordering': ['Services_Name'],
            },
        ),
        migrations.CreateModel(
            name='SuccessStories_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SuccessStories_CategoryType', models.CharField(max_length=100)),
                ('SuccessStories_Cat_Status', models.BooleanField(default=False)),
                ('SuccessStories_Cat_Priority', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)], null=True)),
            ],
            options={
                'verbose_name_plural': 'Success Stories Category',
                'ordering': ['SuccessStories_CategoryType'],
            },
        ),
        migrations.CreateModel(
            name='Tools_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tools_CategoryType', models.CharField(max_length=100)),
                ('Tools_Cat_Status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Tools Category',
                'ordering': ['Tools_CategoryType'],
            },
        ),
        migrations.CreateModel(
            name='Tools_Searched_Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tools_Searched_Title_Name', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name_plural': 'Tools Searched Title Name',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TopMenuItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TopMenuItems_Name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Top Menu Items',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(default=None, max_length=60)),
                ('password', models.CharField(max_length=300)),
                ('Confirm_password', models.CharField(max_length=300)),
                ('phone', models.IntegerField(default=None)),
                ('date', models.DateField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'User',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('userregistration_user_id', models.AutoField(primary_key=True, serialize=False)),
                ('userregistration_first_name', models.CharField(max_length=60)),
                ('userregistration_middle_name', models.CharField(max_length=60)),
                ('userregistration_last_name', models.CharField(max_length=60)),
                ('userregistration_username', models.CharField(blank=True, max_length=60, null=True)),
                ('userregistration_email_field', models.EmailField(max_length=60)),
                ('userregistration_phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('userregistration_address', models.CharField(blank=True, max_length=200, null=True)),
                ('userregistration_password', models.CharField(max_length=30)),
                ('userregistration_confirm_password', models.CharField(max_length=30)),
                ('userregistration_active_status', models.BooleanField(default=False)),
                ('registration_User_Type', models.CharField(choices=[('Individual', 'Individual'), ('Organization', 'Organization'), ('DomainExpert', 'DomainExpert')], default='Individual', max_length=50)),
                ('userregistration_registration_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('userregistration_token', models.CharField(blank=True, max_length=60, null=True)),
            ],
            options={
                'verbose_name_plural': 'User Registration',
                'ordering': ['userregistration_first_name'],
            },
        ),
        migrations.CreateModel(
            name='TranslationQuote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('company_email', models.EmailField(max_length=254, null=True)),
                ('language', models.CharField(max_length=200, null=True)),
                ('domain', models.CharField(max_length=200, null=True)),
                ('delivery_date', models.DateField(null=True)),
                ('client_remark', models.TextField(max_length=50, null=True)),
                ('submission_date', models.DateTimeField(default=datetime.datetime(2022, 7, 15, 1, 9, 44, 817131))),
                ('application_number', models.CharField(max_length=50, null=True)),
                ('total_words', models.IntegerField(null=True)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('translation_delivery_date', models.DateField(null=True)),
                ('quotation_generated_date', models.DateField(null=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('INPROCESS', 'INPROCESS')], default='PENDING', max_length=50, null=True)),
                ('admin_remark', models.TextField(max_length=50, null=True)),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Localisation_App.userregistration', verbose_name='Username')),
            ],
            options={
                'verbose_name_plural': 'Translation Quote',
                'ordering': ['url'],
            },
        ),
        migrations.CreateModel(
            name='ToolsData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ToolsData_HeadingName', models.CharField(max_length=100)),
                ('ToolsData_Description', ckeditor.fields.RichTextField()),
                ('ToolsData_fileSize', models.CharField(default='', max_length=30)),
                ('ToolsData_VersionNumber', models.IntegerField()),
                ('ToolsData_UploadSupportDocument', models.FileField(blank=True, null=True, upload_to='Localisation_App/ToolsDocument')),
                ('ToolsData_UploadToolCode', models.FileField(blank=True, null=True, upload_to='Localisation_App/ToolsCode')),
                ('ToolsData_UploadedDate', models.DateTimeField(auto_now_add=True)),
                ('ToolsData_LastUpdatedDate', models.DateTimeField(auto_now=True, null=True)),
                ('ToolsData_DownloadCounter', models.IntegerField()),
                ('ToolsData_PublishedStatus', models.CharField(choices=[('Published', 'PUBLISHED'), ('Unpublished', 'UNPUBLISHED')], default='published', max_length=20)),
                ('ToolsData_slug', models.SlugField(blank=True, max_length=10000, null=True)),
                ('ToolsData_CategoryType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Localisation_App.tools_category')),
            ],
            options={
                'verbose_name_plural': 'Tools Data',
                'ordering': ['ToolsData_HeadingName'],
            },
        ),
        migrations.CreateModel(
            name='SuccessStories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SuccessStories_TitleName', models.CharField(max_length=100)),
                ('SuccessStories_Link', models.URLField(max_length=100)),
                ('SuccessStories_Description', ckeditor.fields.RichTextField()),
                ('SuccessStories_CreationDate', models.DateTimeField(auto_now_add=True)),
                ('SuccessStories_PublishedDate', models.DateTimeField(auto_now_add=True)),
                ('SuccessStories_LastUpdatedDate', models.DateTimeField(auto_now=True)),
                ('SuccessStories_PublishedStatus', models.CharField(choices=[('Published', 'PUBLISHED'), ('Unpublished', 'UNPUBLISHED')], default='published', max_length=20)),
                ('SuccessStories_Upload_Image_1', models.ImageField(blank=True, null=True, upload_to='Localisation_App/Images')),
                ('SuccessStories_Upload_Image_2', models.ImageField(blank=True, null=True, upload_to='Localisation_App/Images')),
                ('SuccessStories_Upload_Image_3', models.ImageField(blank=True, null=True, upload_to='Localisation_App/Images')),
                ('SuccessStories_Upload_Image_4', models.ImageField(blank=True, null=True, upload_to='Localisation_App/Images')),
                ('SuccessStories_Upload_Image_5', models.ImageField(blank=True, null=True, upload_to='Localisation_App/Images')),
                ('SuccessStories_Cdac_Contribution', models.CharField(blank=True, max_length=500, null=True)),
                ('SuccessStories_Priority', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True)),
                ('SuccessStories_slug', models.SlugField(blank=True, max_length=10000, null=True)),
                ('SuccessStories_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Localisation_App.successstories_category')),
            ],
            options={
                'verbose_name_plural': 'Success Stories',
                'ordering': ['SuccessStories_TitleName'],
            },
        ),
        migrations.CreateModel(
            name='ResourceData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ResourceData_HeadingName', models.CharField(max_length=100)),
                ('ResourceData_Description', ckeditor.fields.RichTextField()),
                ('ResourceData_fileSize', models.CharField(default='', max_length=30)),
                ('ResourceData_VersionNumber', models.IntegerField()),
                ('ResourceData_UploadSupportDocument', models.FileField(blank=True, null=True, upload_to='Localisation_App/ResourceDataDocument')),
                ('ResourceData_UploadResourceCode', models.FileField(blank=True, null=True, upload_to='Localisation_App/ResourceData')),
                ('ResourceData_UploadedDate', models.DateTimeField(auto_now_add=True)),
                ('ResourceData_LastUpdatedDate', models.DateTimeField(auto_now=True, null=True)),
                ('ResourceData_DownloadCounter', models.IntegerField()),
                ('ResourceData_PublishedStatus', models.CharField(choices=[('Published', 'PUBLISHED'), ('Unpublished', 'UNPUBLISHED')], default='published', max_length=20)),
                ('ResourceData_slug', models.SlugField(blank=True, max_length=2000, null=True)),
                ('ResourceData_CategoryType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Localisation_App.resources_category')),
            ],
            options={
                'verbose_name_plural': 'Resource Data',
                'ordering': ['ResourceData_HeadingName'],
            },
        ),
        migrations.CreateModel(
            name='Footer_Links_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Footer_Links_Info_SubTitle', models.CharField(max_length=100)),
                ('Footer_Links_Info_SubContent', ckeditor.fields.RichTextField()),
                ('Footer_Links_Info_MainTitle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Localisation_App.footer_links')),
            ],
            options={
                'verbose_name_plural': 'Footer Info',
                'ordering': ['Footer_Links_Info_SubTitle'],
            },
        ),
        migrations.CreateModel(
            name='FAQs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FAQs_Question', models.CharField(max_length=1000)),
                ('FAQs_Answer', ckeditor.fields.RichTextField()),
                ('FAQs_CategoryType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Localisation_App.faqs_category')),
            ],
            options={
                'verbose_name_plural': 'FAQs',
                'ordering': ['FAQs_Question'],
            },
        ),
        migrations.CreateModel(
            name='EmpanelledAgenciesEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('empanelled_agencies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Localisation_App.empanelledagencies', verbose_name='Empanelled Agency Name')),
            ],
            options={
                'verbose_name_plural': 'Empanelled Agencies Emails',
                'ordering': ['email'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Article_HeadingName', models.CharField(max_length=100)),
                ('Article_Description', ckeditor.fields.RichTextField()),
                ('Article_Image', models.ImageField(null=True, upload_to='Localisation_App/Images')),
                ('Article_CreationDate', models.DateTimeField(auto_now_add=True)),
                ('Article_LastUpdatedDate', models.DateTimeField(auto_now=True)),
                ('Article_PublishedDate', models.DateTimeField(auto_now_add=True)),
                ('Article_PublishedStatus', models.CharField(choices=[('Published', 'PUBLISHED'), ('Unpublished', 'UNPUBLISHED')], default='Unpublished', max_length=20)),
                ('Article_ContentGivenBy', models.CharField(max_length=100)),
                ('Article_MenuId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Localisation_App.topmenuitems')),
            ],
            options={
                'verbose_name_plural': 'Article',
                'ordering': ['Article_HeadingName'],
            },
        ),
    ]
