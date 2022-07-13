from django.contrib import admin
from .models import EmpanelledAgencies, EmpanelledAgenciesEmail, TopMenuItems, Article, SuccessStories, ToolsData, ResourceData, FAQs, NewsAndEvents, Services, FAQs_Category, Tools_Category, Resources_Category, SuccessStories_Category, Footer_Links, Footer_Links_Info, FooterMenuItems, Tools_Searched_Title, Contact, User, UserRegistration, GuidelinceForIndianGovWebsite, TranslationQuote
# Register your models here.


@admin.register(SuccessStories_Category)
class AdminSuccessStories_Category(admin.ModelAdmin):
    list_display = ('SuccessStories_CategoryType',
                    'SuccessStories_Cat_Status')
    list_display_links = ('SuccessStories_CategoryType',
                          'SuccessStories_Cat_Status')
    list_filter = ('SuccessStories_CategoryType', 'SuccessStories_Cat_Status')
    search_fields = ('SuccessStories_CategoryType',
                     'SuccessStories_Cat_Status')
    ordering = ('SuccessStories_CategoryType',)
    list_per_page: int = 20


@admin.register(SuccessStories)
class AdminStories(admin.ModelAdmin):
    list_display = ('SuccessStories_TitleName',
                    'SuccessStories_PublishedStatus', 'SuccessStories_category', 'SuccessStories_Link')
    list_display_links = ('SuccessStories_TitleName',
                          'SuccessStories_PublishedStatus', 'SuccessStories_category', 'SuccessStories_Link')
    list_filter = ('SuccessStories_PublishedStatus',
                   'SuccessStories_category', 'SuccessStories_Link')
    search_fields = ('SuccessStories_TitleName',
                     'SuccessStories_Description', 'SuccessStories_Link')
    ordering = ('SuccessStories_TitleName',)
    list_per_page: int = 20
    save_on_top = True


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    list_display = ('Article_HeadingName', 'Article_MenuId')
    list_display_links = ('Article_HeadingName', 'Article_MenuId')
    list_filter = ('Article_MenuId',)
    search_fields = ('Article_HeadingName',
                     'Article_Description', 'Article_MenuId')
    ordering = ('Article_HeadingName',)
    list_per_page: int = 20


@admin.register(ResourceData)
class AdminResourceData(admin.ModelAdmin):
    list_display = ('ResourceData_HeadingName', 'ResourceData_CategoryType')
    list_display_links = ('ResourceData_HeadingName',
                          'ResourceData_CategoryType')
    list_filter = ('ResourceData_CategoryType',)

    search_fields = ('ResourceData_HeadingName',
                     'ResourceData_Description',)
    ordering = ('ResourceData_HeadingName',)
    list_per_page: int = 20


@admin.register(ToolsData)
class AdminToolsData(admin.ModelAdmin):
    list_display = ('ToolsData_HeadingName', 'ToolsData_CategoryType')
    list_display_links = ('ToolsData_HeadingName', 'ToolsData_CategoryType')
    list_filter = ('ToolsData_CategoryType',)
    search_fields = ('ToolsData_HeadingName',
                     'ToolsData_Description', )
    ordering = ('ToolsData_HeadingName',)


list_per_page: int = 20


@admin.register(FAQs)
class AdminFAQs(admin.ModelAdmin):
    list_display = ('FAQs_Question', 'FAQs_CategoryType')
    list_display_links = ('FAQs_Question', 'FAQs_CategoryType')
    list_filter = ('FAQs_CategoryType',)
    search_fields = ('FAQs_Question', 'FAQs_Answer')
    ordering = ('FAQs_Question',)

    list_per_page: int = 20


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
    list_per_page: int = 20


@admin.register(Services)
class AdminServices(admin.ModelAdmin):
    list_display = ('Services_Name', 'Services_Description')
    list_display_links = ('Services_Name', 'Services_Description')
    list_filter = ('Services_Name',)
    search_fields = ('Services_Name', 'Services_Description')
    ordering = ('Services_Name',)
    list_per_page: int = 20


@admin.register(TopMenuItems)
class AdminTopMenuItems(admin.ModelAdmin):
    list_display = ('TopMenuItems_Name',)
    list_display_links = ('TopMenuItems_Name',)
    list_filter = ('TopMenuItems_Name',)
    search_fields = ('TopMenuItems_Name',)
    ordering = ('id',)
    list_per_page: int = 20


@admin.register(Resources_Category)
class AdminResources_Category(admin.ModelAdmin):
    list_display = ('Resources_CategoryType', 'Resources_Cat_Status',)
    list_display_links = ('Resources_CategoryType', 'Resources_Cat_Status')

    list_filter = ('Resources_CategoryType', 'Resources_Cat_Status')
    search_fields = ('Resources_CategoryType', 'Resources_Cat_Status')
    ordering = ('Resources_CategoryType',)
    list_per_page: int = 20


@admin.register(Tools_Category)
class AdminTools_Category(admin.ModelAdmin):
    list_display = ('Tools_CategoryType', 'Tools_Cat_Status',)
    list_display_links = ('Tools_CategoryType', 'Tools_Cat_Status')
    list_filter = ('Tools_CategoryType', 'Tools_Cat_Status')
    search_fields = ('Tools_CategoryType', 'Tools_Cat_Status')
    ordering = ('Tools_CategoryType',)
    list_per_page: int = 20


@admin.register(FAQs_Category)
class AdminFAQs_Category(admin.ModelAdmin):
    list_display = ('FAQs_CategoryType',)
    list_display_links = ('FAQs_CategoryType',)
    list_filter = ('FAQs_CategoryType',)
    search_fields = ('FAQs_CategoryType',)
    ordering = ('FAQs_CategoryType',)
    list_per_page: int = 20


@admin.register(NewsAndEvents)
class AdminNewsAndEvents(admin.ModelAdmin):
    list_display = ('NewsAndEvents_HeadingName', 'NewsAndEvents_Link',
                    'NewsAndEvents_CreationDate', 'NewsAndEvents_UpdatedDate',)
    list_display_links = ('NewsAndEvents_HeadingName', 'NewsAndEvents_Link',
                          'NewsAndEvents_CreationDate', 'NewsAndEvents_UpdatedDate',)
    list_filter = ('NewsAndEvents_HeadingName',
                   'NewsAndEvents_Link', 'NewsAndEvents_Discription')
    search_fields = ('NewsAndEvents_HeadingName',
                     'NewsAndEvents_Link', 'NewsAndEvents_Discription')
    ordering = ('NewsAndEvents_HeadingName',)
    list_per_page: int = 20


@admin.register(Footer_Links)
class AdminFooter_Links(admin.ModelAdmin):
    list_display = ('Footer_Links_Title', 'Footer_Links_Content',)

    list_display_links = ('Footer_Links_Title', 'Footer_Links_Content',)

    list_filter = ('Footer_Links_Title', 'Footer_Links_Content')
    search_fields = ('Footer_Links_Title', 'Footer_Links_Content')

    ordering = ('Footer_Links_Title',)
    list_per_page: int = 20


@admin.register(Tools_Searched_Title)
class AdminTools_Searched_Title(admin.ModelAdmin):
    list_display = ('Tools_Searched_Title_Name',)
    list_display_links = ('Tools_Searched_Title_Name',)
    list_filter = ('Tools_Searched_Title_Name',)
    search_fields = ('Tools_Searched_Title_Name',)
    ordering = ('Tools_Searched_Title_Name',)
    list_per_page: int = 20


@admin.register(Contact)
class AdminContact(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'option', 'comment')
    list_display_links = ('name', 'email', 'phone', 'option', 'comment')
    list_filter = ('name', 'email', 'option')
    search_fields = ('name', 'email', 'option')
    ordering = ('name',)
    list_per_page: int = 20


@admin.register(UserRegistration)
class AdminUserRegistration(admin.ModelAdmin):
    list_display = ('userregistration_user_id',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(FooterMenuItems)
admin.site.register(TranslationQuote)
admin.site.register(EmpanelledAgencies)
admin.site.register(EmpanelledAgenciesEmail)


@admin.register(GuidelinceForIndianGovWebsite)
class AdminGuidelinceForIndianGovWebsite(admin.ModelAdmin):
    list_display = ('name', 'percentage')


# SANJAY BHARGAVA ADDED BELOW LINES
admin.site.site_header = "Localisation Administration"
admin.site.site_title = "Localisation Administration Portal"
admin.site.index_title = "Welcome to localisation.gov.in Portal"
