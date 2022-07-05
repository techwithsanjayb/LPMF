from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'Localisation_App'
urlpatterns = [
    path('', views.Home, name='Home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('toolsPage/', views.toolsPage, name='toolsPage'),
    path('tools/', views.tools, name='tools'),
    path('toolsSearch/<tools_title>', views.toolsSearch, name='toolsSearch'),
    path('resourcesPage/', views.resourcesPage, name='resourcesPage'),
    path('resources/', views.resources, name='resources'),
    path('resourceSearch/<resource_title>',
         views.resourceSearch, name='resourceSearch'),
    path('services/', views.services, name='services'),
    path('successstoryPage', views.successstoryPage, name='successstoryPage'),
    path('successstory', views.successstory, name='successstory'),
    path('successstorySearch/<story_title>',
         views.successstorySearch, name='successstorySearch'),
    path('submit/', views.submit, name='submit'),
    path('faqs/', views.faqs, name='faqs'),
    path('faqsSearch/<faq_title>', views.faqsSearch, name='faqsSearch'),
    path('contactus/', views.contactus, name='contactus'),
    path('register/', views.faqs, name='register'),
    path('login/', views.faqs, name='login'),
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
    path('goTranslate/', views.goTranslate,
         name='goTranslate'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
