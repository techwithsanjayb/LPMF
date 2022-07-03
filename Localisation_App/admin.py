from django.contrib import admin
from .models import TopMenuItems, Article, SuccessStories, ToolsData, ResourceData, FAQs, NewsAndEvents, Services, FAQs_Category, Tools_Category, Resources_Category, SuccessStrories_Category, Footer_Links, Footer_Links_Info, FooterMenuItems, Tools_Searched_Title, Contact, User
# Register your models here.


@admin.register(SuccessStories)
class AdminStories(admin.ModelAdmin):
    list_display = ('SuccessStories_TitleName',
                    'SuccessStories_PublishedStatus', 'SuccessStories_category')
    list_display_links = ('SuccessStories_TitleName',
                          'SuccessStories_PublishedStatus', 'SuccessStories_category')
    list_filter = ('SuccessStories_PublishedStatus', 'SuccessStories_category')
    search_fields = ('SuccessStories_TitleName', 'SuccessStories_Description')
    ordering = ('SuccessStories_TitleName',)
    list_per_page: int = 10


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    list_display = ('Article_HeadingName', 'Article_MenuId')
    list_display_links = ('Article_HeadingName', 'Article_MenuId')
    list_filter = ('Article_MenuId',)
    search_fields = ('Article_HeadingName', 'Article_Description')
    ordering = ('Article_HeadingName',)
    list_per_page: int = 10


@admin.register(ResourceData)
class AdminResourceData(admin.ModelAdmin):
    list_display = ('ResourceData_HeadingName', 'ResourceData_CategoryType')
    list_display_links = ('ResourceData_HeadingName',
                          'ResourceData_CategoryType')
    list_filter = ('ResourceData_CategoryType',)
    search_fields = ('ResourceData_HeadingName', 'ResourceData_Description')
    ordering = ('ResourceData_HeadingName',)
    list_per_page: int = 10


@admin.register(ToolsData)
class AdminToolsData(admin.ModelAdmin):
    list_display = ('ToolsData_HeadingName', 'ToolsData_CategoryType')
    list_display_links = ('ToolsData_HeadingName', 'ToolsData_CategoryType')
    list_filter = ('ToolsData_CategoryType',)
    search_fields = ('ToolsData_HeadingName', 'ToolsData_Description')
    ordering = ('ToolsData_HeadingName',)


list_per_page: int = 10


@admin.register(FAQs)
class AdminFAQs(admin.ModelAdmin):
    list_display = ('FAQs_Question', 'FAQs_CategoryType')
    list_display_links = ('FAQs_Question', 'FAQs_CategoryType')
    list_filter = ('FAQs_CategoryType',)
    search_fields = ('FAQs_Question', 'FAQs_Answer')
    ordering = ('FAQs_Question',)

    list_per_page: int = 10


@admin.register(Footer_Links_Info)
class AdminFooter_Links_Info(admin.ModelAdmin):
    list_display = ('Footer_Links_Info_SubTitle',
                    'Footer_Links_Info_MainTitle')
    list_display_links = ('Footer_Links_Info_SubTitle',
                          'Footer_Links_Info_MainTitle')
    list_filter = ('Footer_Links_Info_MainTitle',)
    search_fields = ('Footer_Links_Info_SubTitle',
                     'Footer_Links_Info_MainTitle')
    ordering = ('Footer_Links_Info_SubTitle',)
    list_per_page: int = 10


@admin.register(Services)
class AdminServices(admin.ModelAdmin):
    list_display = ('Services_Name', 'Services_Description')
    list_display_links = ('Services_Name', 'Services_Description')
    list_filter = ('Services_Name',)
    search_fields = ('Services_Name', 'Services_Description')
    ordering = ('Services_Name',)
    list_per_page: int = 10


admin.site.register(TopMenuItems)
admin.site.register(SuccessStrories_Category)
admin.site.register(Resources_Category)
admin.site.register(Tools_Category)
admin.site.register(FAQs_Category)
admin.site.register(NewsAndEvents)
admin.site.register(FooterMenuItems)
admin.site.register(Footer_Links)
admin.site.register(Tools_Searched_Title)
admin.site.register(Contact)
admin.site.register(User)


# SANJAY BHARGAVA ADDED BELOW LINES

admin.site.site_header = "Localisation Administration"
admin.site.site_title = "Localisation Administration Portal"
admin.site.index_title = "Welcome to localisation.gov.in Portal"
