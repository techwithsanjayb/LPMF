from pyexpat import model
from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator
# Create your models here.

'''
    AUTHOR NAME      : Sanjay Bhargava
    CREATED DATE     : 14-05-2022
    MODEL NAME       : TopMenuItems
    DISCRIPTION      : THE BELOW MODEL STORES TOP MENU ITEMS NAME APPEARING ON THE TOP OF PAGES.
'''


class TopMenuItems(models.Model):
    TopMenuItems_Name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Top Menu Items"
        ordering = ['id']

    def __str__(self):
        return self.TopMenuItems_Name


'''
    AUTHOR NAME      : Shubhangni Asati, Shweta Patil, Abhijeet Thorat
    CREATED DATE     : 15-05-2022
    MODEL NAME       : Article
    DISCRIPTION      : THE BELOW MODEL STORES TEXT CONTENT FOR THE ARTICLES OF THE DIFFERENT PAGES OF WEBSITE.
'''


class Article(models.Model):
    Article_HeadingName = models.CharField(max_length=100)
    Article_Description = RichTextField()
    Article_Image = models.ImageField(
        upload_to="Localisation_App/Images", height_field=None, width_field=None, max_length=None, null=True)
    Article_CreationDate = models.DateTimeField(auto_now_add=True,  blank=True)
    Article_LastUpdatedDate = models.DateTimeField(auto_now=True,  blank=True)
    Article_PublishedDate = models.DateTimeField(
        auto_now_add=True,  blank=True)
    Article_PublishedStatus = (
        ('Published', 'PUBLISHED'), ('Unpublished', 'UNPUBLISHED'))
    Article_PublishedStatus = models.CharField(
        max_length=20, choices=Article_PublishedStatus, default="Unpublished")
    Article_ContentGivenBy = models.CharField(max_length=100)
    Article_MenuId = models.ForeignKey(TopMenuItems, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Article"
        ordering = ['Article_HeadingName']

    def __str__(self):
        return self.Article_HeadingName


'''
    AUTHOR NAME      : Shubhangni Asati, Shweta Patil, Abhijeet Thorat
    CREATED DATE     : 15-05-2022
    MODEL NAME       : Article
    DISCRIPTION      : THE BELOW MODEL STORES SUCCESS STORIES DATA FOR THE LOCALISATION PORTAL.
'''


class SuccessStories_Category(models.Model):
    SuccessStories_CategoryType = models.CharField(max_length=100)
    SuccessStories_Cat_Status = models.BooleanField(default=False)

    CHOICES1 = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)]
    SuccessStories_Cat_Priority = models.IntegerField(
        choices=CHOICES1, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Success Stories Category"
        ordering = ['SuccessStories_CategoryType']

    def __str__(self):
        return self.SuccessStories_CategoryType


class SuccessStories(models.Model):
    SuccessStories_TitleName = models.CharField(max_length=100)
    SuccessStories_Link = models.URLField(max_length=100)
    SuccessStories_Description = RichTextField()
    SuccessStories_CreationDate = models.DateTimeField(
        auto_now_add=True,  blank=True)
    SuccessStories_PublishedDate = models.DateTimeField(
        auto_now_add=True,  blank=True)
    SuccessStories_LastUpdatedDate = models.DateTimeField(
        auto_now=True,  blank=True)
    SuccessStories_PublishedStatus = (
        ('Published', 'PUBLISHED'), ('Unpublished', 'UNPUBLISHED'))
    SuccessStories_PublishedStatus = models.CharField(
        max_length=20, choices=SuccessStories_PublishedStatus, default="Unpublished")
    SuccessStories_Upload_Image_1 = models.ImageField(
        upload_to="Localisation_App/Images", height_field=None, width_field=None, max_length=None, null=True, blank=True)

    SuccessStories_Upload_Image_2 = models.ImageField(
        upload_to="Localisation_App/Images", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    SuccessStories_Upload_Image_3 = models.ImageField(
        upload_to="Localisation_App/Images", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    SuccessStories_Upload_Image_4 = models.ImageField(
        upload_to="Localisation_App/Images", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    SuccessStories_Upload_Image_5 = models.ImageField(
        upload_to="Localisation_App/Images", height_field=None, width_field=None, max_length=None, null=True, blank=True)

    SuccessStories_category = models.ForeignKey(
        SuccessStories_Category, on_delete=models.CASCADE, null=True, blank=True)

    SuccessStories_Cdac_Contribution = models.CharField(
        max_length=500, null=True, blank=True)

    CHOICES1 = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]
    SuccessStories_Priority = models.IntegerField(
        choices=CHOICES1, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Success Stories"
        ordering = ['SuccessStories_TitleName']

    def __str__(self):
        return self.SuccessStories_TitleName


class Tools_Category(models.Model):
    Tools_CategoryType = models.CharField(max_length=100)
    Tools_Cat_Status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Tools Category"
        ordering = ['Tools_CategoryType']

    def __str__(self):
        return self.Tools_CategoryType


class Tools_Searched_Title(models.Model):
    Tools_Searched_Title_Name = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "Tools Searched Title Name"
        ordering = ['id']

    def __str__(self):
        return self.Tools_Searched_Title_Name


class ToolsData(models.Model):
    ToolsData_HeadingName = models.CharField(max_length=100)
    ToolsData_Description = RichTextField()
    ToolsData_CategoryType = models.ForeignKey(
        Tools_Category, on_delete=models.CASCADE)
    ToolsData_fileSize = models.CharField(max_length=30, default="")
    ToolsData_VersionNumber = models.IntegerField()
    ToolsData_UploadSupportDocument = models.FileField(
        upload_to="Localisation_App/ToolsDocument", null=True, blank=True)
    ToolsData_UploadToolCode = models.FileField(
        upload_to="Localisation_App/ToolsCode", null=True, blank=True)
    ToolsData_UploadedDate = models.DateTimeField(
        auto_now_add=True,  blank=True)
    ToolsData_LastUpdatedDate = models.DateTimeField(
        auto_now=True, blank=True, null=True)
    ToolsData_DownloadCounter = models.IntegerField()

    class Meta:
        verbose_name_plural = "Tools Data"
        ordering = ['ToolsData_HeadingName']

    def __str__(self):
        return self.ToolsData_HeadingName


class Resources_Category(models.Model):
    Resources_CategoryType = models.CharField(max_length=100)
    Resources_Cat_Status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Resources Category"
        ordering = ['Resources_CategoryType']

    def __str__(self):
        return self.Resources_CategoryType


class ResourceData(models.Model):
    ResourceData_HeadingName = models.CharField(max_length=100)
    ResourceData_Description = RichTextField()
    ResourceData_CategoryType = models.ForeignKey(
        Resources_Category, on_delete=models.CASCADE)
    ResourceData_fileSize = models.CharField(max_length=30, default="")
    ResourceData_VersionNumber = models.IntegerField()
    ResourceData_UploadSupportDocument = models.FileField(
        upload_to="Localisation_App/ResourceDataDocument", null=True, blank=True)
    ResourceData_UploadResourceCode = models.FileField(
        upload_to="Localisation_App/ResourceData", null=True, blank=True)
    ResourceData_UploadedDate = models.DateTimeField(
        auto_now_add=True,  blank=True)
    ResourceData_LastUpdatedDate = models.DateTimeField(
        auto_now=True, blank=True, null=True)
    ResourceData_DownloadCounter = models.IntegerField()

    class Meta:
        verbose_name_plural = "Resource Data"
        ordering = ['ResourceData_HeadingName']

    def __str__(self):
        return self.ResourceData_HeadingName


class NewsAndEvents(models.Model):
    NewsAndEvents_HeadingName = models.CharField(max_length=100)
    NewsAndEvents_CreationDate = models.DateTimeField(
        auto_now=True,  blank=True)
    NewsAndEvents_UpdatedDate = models.DateTimeField(
        auto_now_add=True,  blank=True)
    NewsAndEvents_Link = models.URLField(max_length=200)

    class Meta:
        verbose_name_plural = "News And Events"
        ordering = ['NewsAndEvents_HeadingName']

    def __str__(self):
        return self.NewsAndEvents_HeadingName


class FAQs_Category(models.Model):
    FAQs_CategoryType = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "FAQs Category"
        ordering = ['FAQs_CategoryType']

    def __str__(self):

        return self.FAQs_CategoryType


class FAQs(models.Model):
    FAQs_Question = models.CharField(max_length=1000)
    FAQs_Answer = RichTextField()
    FAQs_CategoryType = models.ForeignKey(
        FAQs_Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "FAQs"
        ordering = ['FAQs_Question']

    def __str__(self):
        return self.FAQs_Question


class Services(models.Model):
    Services_Name = models.CharField(max_length=100)
    Services_Description = models.CharField(max_length=300)
    Services_links = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = "Services"
        ordering = ['Services_Name']

    def __str__(self):
        return self.Services_Name


class Footer_Links(models.Model):
    Footer_Links_Title = models.CharField(max_length=100)
    Footer_Links_Content = RichTextField()

    class Meta:
        verbose_name_plural = "Footer Links"
        ordering = ['Footer_Links_Title']

    def __str__(self):
        return self.Footer_Links_Title


class Footer_Links_Info(models.Model):
    Footer_Links_Info_SubTitle = models.CharField(max_length=100)
    Footer_Links_Info_SubContent = RichTextField()
    Footer_Links_Info_MainTitle = models.ForeignKey(
        Footer_Links, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Footer Info"
        ordering = ['Footer_Links_Info_SubTitle']

    def __str__(self):
        return self.Footer_Links_Info_SubTitle


class FooterMenuItems(models.Model):
    FooterMenuItems_Name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Footer Menu Items"
        ordering = ['id']

    def __str__(self):
        return self.FooterMenuItems_Name


'''
    AUTHOR NAME      : TANVI PATIL
    CREATED DATE     : 21-06-2022
    MODEL NAME       : Contact Us
    DISCRIPTION      : THE BELOW MODEL STORES CONTACT US DATA FOR THE LOCALISATION PORTAL.
'''


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    option = models.CharField(max_length=30)
    comment = models.TextField()

    class Meta:
        verbose_name_plural = "Contact Us"
        ordering = ['name']

    def __str__(self):
        return self.option


class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=60, default=None)
    password = models.CharField(max_length=300)
    Confirm_password = models.CharField(max_length=300)
    phone = models.IntegerField(default=None)
    date = models.DateField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "User"
        ordering = ['name']

    def __str__(self):
        return self.name


class CarouselData(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)
    caption = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Carousel Data"
        ordering = ['title']

    def __str__(self):
        return self.title


'''
    AUTHOR NAME      : SHWETA PATIL
    CREATED DATE     : 05-07-2022
    MODEL NAME       : UserRegistration
'''


# USER_REGISTRATION TABLES MODEL


class UserRegistration(models.Model):
    userregistration_user_id = models.AutoField(primary_key=True)
    userregistration_first_name = models.CharField(max_length=60)
    userregistration_middle_name = models.CharField(max_length=60)
    userregistration_last_name = models.CharField(max_length=60)
    userregistration_username = models.CharField(
        max_length=60, blank=True, null=True)
    userregistration_email_field = models.EmailField(
        max_length=60)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    userregistration_phone_number = models.CharField(
        validators=[phone_regex], max_length=17)  # Validators should be a list
    userregistration_address = models.CharField(
        max_length=200, blank=True, null=True)
    userregistration_password = models.CharField(max_length=30)
    userregistration_confirm_password = models.CharField(max_length=30)
    userregistration_active_status = models.BooleanField(default=False)
    CHOICES = [('Individual', 'Individual'),
               ('Organization', 'Organization'),
               ('DomainExpert', 'DomainExpert')]
    registration_User_Type = models.CharField(
        max_length=50, choices=CHOICES, default='Individual')
    userregistration_registration_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "User Registration"
        ordering = ['userregistration_first_name']

    def __str__(self):
        return self.userregistration_first_name + " " + self.userregistration_last_name


# translation quote

class TranslationQuote(models.Model):
    url = models.URLField(max_length=200)
    language = models.CharField(max_length=200)
    website_type = models.CharField(max_length=200, null=True)
    delivery_date = models.DateField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = "Translation Quote"
        ordering = ['url']

    def __str__(self):
        return self.url

class GuidelinceForIndianGovWebsite(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.IntegerField()
    class Meta:
        verbose_name_plural = "Guidelince For Indian Gov Website"
    def __str__(self):
        return self.name 
