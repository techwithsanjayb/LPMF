from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views


app_name = 'Localisation_App'
urlpatterns = [
    path('', views.Home, name='Home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('toolsPage/', views.toolsPage, name='toolsPage'),
    path('tools/', views.tools, name='tools'),
    path('toolsDownloadCounter/<int:id>', views.toolsDownloadCounter, name='toolsDownloadCounter'),
    path('toolsReset/', views.toolsReset, name='toolsReset'),
    path('toolsSearch/<tools_title>', views.toolsSearch, name='toolsSearch'),
    path('resourcesPage/', views.resourcesPage, name='resourcesPage'),
    path('resources/', views.resources, name='resources'),
    path('resourceDownloadCounter/<int:id>', views.resourceDownloadCounter, name='resourceDownloadCounter'),
    path('resourcesReset/', views.resourcesReset, name='resourcesReset'),
    path('resourceSearch/<slug:resource_title>',
         views.resourceSearch, name='resourceSearch'),
    path('services/', views.services, name='services'),
    path('successstoryPage/', views.successstoryPage, name='successstoryPage'),
    path('successstory/', views.successstory, name='successstory'),
    path('successstorySearch/<story_title>',
         views.successstorySearch, name='successstorySearch'),
    path('successstoryReset/', views.successstoryReset, name='successstoryReset'),
    path('submit/', views.submit, name='submit'),
    path('faqs/', views.faqs, name='faqs'),
    path('faqsSearch/<faq_title>', views.faqsSearch, name='faqsSearch'),
    path('contactus/', views.contactus, name='contactus'),
    path('base/', views.topmenu, name='base'),
    path('websitepolicy/', views.websitepolicy, name='websitepolicies'),
    path('websitepolicy/<int:id>', views.websitepolicydata,
         name='websitepolicydata'),
    path('termsandcondition/', views.termsandcondition, name='termsandcondition'),
    path('accessibilityStatement/', views.accessibilityStatement,
         name='accessibilityStatement'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('help/', views.help, name='help'),
    path('test/', views.Test, name='test'),
    path('submit/<img>', views.submit, name='submit'),
    path('help/<int:id>', views.helpData, name='helpData'),
    path('ServicesDemoPage/', views.ServicesDemoPage, name='ServicesDemoPage'),
    path('srvEnableTyping/', views.srvEnableTyping, name='srvEnableTyping'),
    path('srvGoTranslateWebLocalizer/', views.srvGoTranslateWebLocalizer,
         name='srvGoTranslateWebLocalizer'),
    path('srvOnscreenKeyboard/', views.srvOnscreenKeyboard,
         name='srvOnscreenKeyboard'),
    path('srvTTS/', views.srvTTS, name='srvTTS'),
    path('srvTransliteration/', views.srvTransliteration,
         name='srvTransliteration'),


    path('register/', views.Register_user, name="register"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('forgetPassword/', views.forgetPassword, name='forgetPassword'),
    path('changePassword/<token>/', views.changePassword, name='changePassword'),
    #     path('logout_user/', views.logout_user, name="logout"),
    #   path('register/', views.Register_user, name="register"),

    path('goTranslate/', views.goTranslate,
         name='goTranslate'),
    path('translation-quote/', views.translation_quote,
         name='translation_quote'),
    path('translation_quote_user_dashboard', views.translation_quote_user_dashboard, name='translation_quote_user_dashboard'),
    path('translation_quote_show/<str:application_number>/', views.translation_quote_show, name='translation_quote_show'),
    path('dashboard2', views.dashboard2, name="dashboard2"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('machine-translation/', views.machine_translation, name="machine_translation"),
    path('name-matcher/', views.name_matcher, name="name_matcher"),
    path('empanelled_agencies/', views.empanelled_agencies, name="empanelled_agencies"),
    
    
#     path("Slug_test/<slug:slug>", views.Slug_test, name="Slug_test"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
