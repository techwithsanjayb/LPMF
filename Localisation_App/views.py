from threading import currentThread
from wsgiref import validate
from django.db.models import Sum
from django.forms import ValidationError
from Localisation_Project.settings import CACHE_TTL
from .forms import TTSservice, RegisterForm, TranslationQuoteForm, UserLoginForm, UserChangePasswordForm, UserForgetPasswordForm
from django.contrib import messages
from django.core.mail import send_mail, mail_admins
from django.core.paginator import Paginator
from multiprocessing import context
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models import *
import random
import requests
from .word_count import crawl_data
from django.contrib.auth.models import User
import uuid
from datetime import date, datetime
from .helpers import send_forget_password_email
import json
from bson import json_util
from django.urls import resolve
import uuid
from django.contrib.auth.decorators import login_required
import logging
from datetime import date
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core import validators
logger = logging.getLogger('django')
global str_num
global url
CACHE_TTL = getattr(settings,'CACHE_TTL',DEFAULT_TIMEOUT)


# Home Page

def Home(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        print("url", url)
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        if cache.get("All_Article_data"):
            articleData = cache.get("All_Article_data")
            print("cache data")
        else:
            articleData = Article.objects.all()
            cache.set("All_Article_data", articleData)
            print("database data")

        if cache.get("All_SuccessStories_data"):
            successStoriesData = cache.get("All_SuccessStories_data")
            print("cache data")
        else:
            successStoriesData = SuccessStories.objects.all()
            cache.set("All_SuccessStories_data", successStoriesData)
            print("database data")

        if cache.get("All_Services_data"):
            servicesdata = cache.get("All_Services_data")
            print("cache data")
        else:
            servicesdata = Services.objects.all()
            cache.set("All_Services_data", servicesdata)
            print("database data")

        if cache.get("All_NewsAndEvents_data"):
            newsAndEventsData = cache.get("All_NewsAndEvents_data")
            print("cache data")
        else:
            newsAndEventsData = NewsAndEvents.objects.all()
            cache.set("All_NewsAndEvents_data", newsAndEventsData)
            print("database data")
        logger.info("Home page is getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'ArticleData': articleData,
            'SuccessStoriesData': successStoriesData,
            'NewsAndEventsData': newsAndEventsData,
            'Servicesdata': servicesdata
        }
        return render(request, 'Localisation_App/home.html', context)
    except:
        return render(request, "Localisation_App/serverdown.html")



# About Us Page

def aboutus(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        print("hello")
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        if cache.get("All_About_data"):
            articleData = cache.get("All_About_data")
            print("cache data")
        else:
            articleData = Article.objects.all().filter(Article_HeadingName="About Us")
            cache.set("All_About_data", articleData)
            print("database data")
        logger.info("About Us page is getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'ArticleData': articleData,
        }
        return render(request, 'Localisation_App/aboutus.html', context)
    except:
        return render(request, "Localisation_App/serverdown.html")

# Tools Page

def toolsPage(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        if cache.get("All_ToolsData_data"):
            tools_Data=cache.get("All_ToolsData_data")
            print("cache data")
        else:
            tools_Data = ToolsData.objects.all()
            cache.set("All_ToolsData_data",tools_Data)
            print("database data")
        Tools_Category.objects.all().update(Tools_Cat_Status=False)
        if cache.get("All_ToolsCategory_data"):
            toolsCategory_data=cache.get("All_ToolsCategory_data")
            print("cache data")
        else:
            toolsCategory_data = Tools_Category.objects.all()
            cache.set("All_ToolsCategory_data",toolsCategory_data)
            print("database data")
        count = ToolsData.objects.all().count()
        page = Paginator(tools_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = tools_Data.count()
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'toolsdata': tools_Data,
            'tools_title': 'none',
            'toolscategory': toolsCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count,
            'form': UserLoginForm()
        }
        logger.info("Tools page getting displayed")
        # if request.user.is_authenticated:
        #     return render(request, 'Localisation_App/tools.html', context)
        # else:
        return render(request, 'Localisation_App/tools.html', context)
    except:
        return render(request, "Localisation_App/serverdown.html")


def tools(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        checklist1 = []
        category_name = []
        pagestatus = False
        filtered_Tools_Data = ToolsData.objects.none()
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        if cache.get("All_ToolsData_data1"):
            tools_Data=cache.get("All_ToolsData_data1")
            print("cache data")
        else:
            tools_Data = ToolsData.objects.all()
            cache.set("All_ToolsData_data1",tools_Data)
            print("database data")
        
        toolsCategory_data = Tools_Category.objects.all()
        
        count = ToolsData.objects.all().count()

        if request.method == "POST":
            if request.POST.get('all_checkbox') != 'all_Checked':
                category_name = []
                filtered_Tools_Data = ToolsData.objects.none()
                print("dumydata", filtered_Tools_Data)
                checklist = request.POST.getlist('checkbox')
                Tools_Category.objects.all().update(Tools_Cat_Status=False)
                try:
                    for cat_check in checklist:
                        Tools_Category.objects.filter(
                            pk=int(cat_check)).update(Tools_Cat_Status=True)
                    checklist.append(10101010110101010101)
                    print("string",checklist)
                    if cache.get(checklist):
                        toolsData_Checked=cache.get(checklist)
                        logger.info("Inside tools function, fetching Tools_Category data by selected category ids through cache")
                    else:
                        toolsData_Checked = Tools_Category.objects.filter(id__in=checklist)
                        cache.set(checklist,toolsData_Checked)
                        logger.info("Inside tools function, fetching Tools_Category data by selected category ids through database")
                except:
                    page = Paginator(tools_Data, 8)
                    Tools_Category.objects.all().update(Tools_Cat_Status=False)
                    page_list = request.GET.get('page')
                    page = page.get_page(page_list)
                    count = ToolsData.objects.all().count()
                    print("Inside tools function, error in fetching Tools_Category data by selected category ids")
                    logger.error("Inside tools function, error in fetching Tools_Category data by selected category ids")
                    context = {
                            'topmenus': top_menu_items_data,
                            'FooterMenuItemsdata': footer_menu_items_data,
                            'toolsdata': tools_Data,
                            'tools_title': 'none',
                            'toolscategory': toolsCategory_data,
                            "page": page,
                            'status_All_Checked': 'True',
                            'Pagination_Type': 'All_Data',
                            'count': count
                        }
                    return render(request,'Localisation_App/tools.html', context)       
        
                try:
                    for cat_check_name in toolsData_Checked:
                        # print('hello',n.Tools_CategoryType)
                        category_name.append(cat_check_name.Tools_CategoryType)
                    # print("list",category_name)
                    # print("tuple",tuple(category_name))
                    category_name.append("ToFetch_FilteredTools_With_Cache")
                    to_fetch = tuple(category_name)

                    if cache.get(to_fetch):
                        filtered_Tools_Data=cache.get(to_fetch)
                        logger.info("Inside tools function,fetching Tools_Data data by selected category name through cache")
                    else:
                        for cat_name in to_fetch:
                            filtered_Tools_Data = filtered_Tools_Data | ToolsData.objects.filter(
                                ToolsData_CategoryType__Tools_CategoryType__contains=cat_name)
                        cache.set(to_fetch,filtered_Tools_Data)
                        logger.info("Inside tools function,fetching Tools_Data data by selected category name through database") 
                except:
                    page = Paginator(tools_Data, 8)
                    Tools_Category.objects.all().update(Tools_Cat_Status=False)
                    page_list = request.GET.get('page')
                    page = page.get_page(page_list)
                    count = ToolsData.objects.all().count()
                    print("Inside tools function, error in fetching Tools_Data data by selected category name")
                    logger.error("Inside tools function, error in fetching Tools_Data data by selected category name")
                    context = {
                            'topmenus': top_menu_items_data,
                            'FooterMenuItemsdata': footer_menu_items_data,
                            'toolsdata': tools_Data,
                            'tools_title': 'none',
                            'toolscategory': toolsCategory_data,
                            "page": page,
                            'status_All_Checked': 'True',
                            'Pagination_Type': 'All_Data',
                            'count': count
                        }
                    return render(request,'Localisation_App/tools.html', context)

                count = filtered_Tools_Data.count()
                page = Paginator(filtered_Tools_Data, 8)
                page_list = request.GET.get('page')
                # print("pagenumber",page_list)
                page = page.get_page(page_list)
                logger.info("Tools page getting displayed with selected category filteration")
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'toolsdata': filtered_Tools_Data,
                    'tools_title': 'none',
                    'toolscategory': toolsCategory_data,
                    "page": page,
                    'status_All_Checked': None,
                    'Pagination_Type': 'Category_Post',
                    'count': count
                }
                print("inside 1")
                # return render(request,'Localisation_App/tools.html',context)
                return render(request, 'Localisation_App/tools.html', context)
            else:
                logger.info(
                    "Tools page getting displayed with all category filteration")
                page = Paginator(tools_Data, 8)
                Tools_Category.objects.all().update(Tools_Cat_Status=False)
                page_list = request.GET.get('page')
                page = page.get_page(page_list)
                count = ToolsData.objects.all().count()
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'toolsdata': tools_Data,
                    'tools_title': 'none',
                    'toolscategory': toolsCategory_data,
                    "page": page,
                    'status_All_Checked': 'True',
                    'Pagination_Type': 'All_Data',
                    'count': count
                }
                print("inside 2")
                return render(request, 'Localisation_App/tools.html', context)
        try:
            for category in toolsCategory_data:
                if category.Tools_Cat_Status == True:
                    print("true")
                    pagestatus = True
                    category_name.append(category.Tools_CategoryType)
            category_name.append("ToFetch_FilteredTools_With_Cache")
            to_fetch = tuple(category_name)
            if cache.get(to_fetch):
                filtered_Tools_Data=cache.get(to_fetch)
                logger.info("Inside tools function,fetching Tools_Data data by selected category name through cache for pagination")
            else:
                for cat_name in to_fetch:
                    filtered_Tools_Data = filtered_Tools_Data | ToolsData.objects.filter(
                        ToolsData_CategoryType__Tools_CategoryType__contains=cat_name)
                cache.set(to_fetch,filtered_Tools_Data)
                logger.info("Inside tools function,fetching Tools_Data data by selected category name through database for pagination") 
                
        except:
            print("Inside tools function for pagination, error in fetching Tools_Data data by selected category name")
            logger.error("Inside tools function for pagination, error in fetching Tools_Data data by selected category name")
            page = Paginator(tools_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = tools_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'toolsdata': tools_Data,
                'tools_title': 'none',
                'toolscategory': toolsCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
            # print("toolssaerchedvalue",Tools_Searched_Value)
            return render(request, 'Localisation_App/tools.html', context)

        if pagestatus == True:
            logger.info(
                "Tools page getting displayed with selected category filteration and pagination")
            page = Paginator(filtered_Tools_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = filtered_Tools_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'toolsdata': filtered_Tools_Data,
                'tools_title': 'none',
                'toolscategory': toolsCategory_data,
                "page": page,
                'status_All_Checked': None,
                'Pagination_Type': 'Category_Post',
                'count': count
            }

        else:
            logger.info(
                "Tools page getting displayed with all category filteration and pagination")
            page = Paginator(tools_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = tools_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'toolsdata': tools_Data,
                'tools_title': 'none',
                'toolscategory': toolsCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
        # print("toolssaerchedvalue",Tools_Searched_Value)
        return render(request, 'Localisation_App/tools.html', context)
    except:
        return render(request, "Localisation_App/serverdown.html")


def toolsSearch(request, tools_title):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        tools_searchData = tools_title.replace(" ", "-")
        print("titlenone", tools_title)
        print("replace space ", tools_title.replace(" ", "-"))
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        
        if cache.get("All_ToolsData_data1"):
            tools_Data=cache.get("All_ToolsData_data1")
            print("cache data")
        else:
            tools_Data = ToolsData.objects.all()
            cache.set("All_ToolsData_data1",tools_Data)
            print("database data")
        
        if cache.get("All_ToolsCat_Searcheddata"):
            toolsCategory_data=cache.get("All_ToolsCat_Searcheddata")
            print("cache data")
        else:
            toolsCategory_data = Tools_Category.objects.all()
            cache.set("All_ToolsCat_Searcheddata",toolsCategory_data)
            print("database data")

        if request.method == "POST":
            try:
                print("insideSearchMethod")
                print(tools_title)
                tools_title12 = request.POST.get("toolname")
                print("resourcestitle", tools_title12)
                tools_searchData1 = tools_title12.replace(" ", "-")
                if tools_searchData1 != '':
                    Tools_search=url+tools_searchData1
                    if cache.get(Tools_search):
                        tools_Data=cache.get(Tools_search)
                        logger.info("Inside toolsSearch function,fetching Tools_Data data by search data through cache")
                    else:
                        tools_Data = ToolsData.objects.filter(ToolsData_slug__icontains=tools_searchData1)
                        cache.set(Tools_search,tools_Data)
                        logger.info("Inside toolsSearch function,fetching Tools_Data data by search data through database")
                
                    count = tools_Data.count()
                    print("datatooldssds", count)
                    page = Paginator(tools_Data, 8)
                    page_list = request.GET.get('page')
                    # print("pagenumber",page_list)
                    page = page.get_page(page_list)
                    logger.info(
                        "Tools page getting displayed with searched tools data by slugs")
                    context = {
                        'topmenus': top_menu_items_data,
                        'FooterMenuItemsdata': footer_menu_items_data,
                        'toolsdata': tools_Data,
                        'tools_title': tools_searchData1,
                        'toolscategory': toolsCategory_data,
                        "page": page,
                        'status_All_Checked': 'True',
                        'Pagination_Type': 'Searched_Post',
                        'count': count
                    }
                else:
                    logger.info("Tools page getting displayed with all tools data")
                    page = Paginator(tools_Data, 8)
                    page_list = request.GET.get('page')
                    page = page.get_page(page_list)
                    count = tools_Data.count()
                    print("None Selected")
                    context = {
                        'topmenus': top_menu_items_data,
                        'FooterMenuItemsdata': footer_menu_items_data,
                        'toolsdata': tools_Data,
                        'tools_title': 'none',
                        'toolscategory': toolsCategory_data,
                        "page": page,
                        'status_All_Checked': 'True',
                        'Pagination_Type': 'Searched_Post',
                        'count': count
                    }
                return render(request, 'Localisation_App/tools.html', context)
            except:
                logger.error("toolsSearch function, getting wrong input search data")
                page = Paginator(tools_Data, 8)
                page_list = request.GET.get('page')
                page = page.get_page(page_list)
                count = tools_Data.count()
                print("None Selected")
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'toolsdata': tools_Data,
                    'tools_title': 'none',
                    'toolscategory': toolsCategory_data,
                    "page": page,
                    'status_All_Checked': 'True',
                    'Pagination_Type': 'Searched_Post',
                    'count': count
                }
                return render(request, 'Localisation_App/tools.html', context)

        if tools_searchData != 'none':
            logger.info(
                "Tools page getting displayed with searched tools data by slugs")
            Tools_search1=url+tools_searchData
            if cache.get(Tools_search1):
                tools_Data1=cache.get(Tools_search1)
                logger.info("Inside toolsSearch function,fetching Tools_Data data by search data through cache for pagination")
            else:
                tools_Data1 = ToolsData.objects.filter(ToolsData_slug__icontains=tools_searchData)
                cache.set(Tools_search1,tools_Data1)
                logger.info("Inside toolsSearch function,fetching Tools_Data data by search data through database for pagination")
            page = Paginator(tools_Data1, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = tools_Data1.count()
            print("hereee", tools_Data1)
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'toolsdata': tools_Data1,
                'tools_title': tools_searchData,
                'toolscategory': toolsCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        else:
            logger.info("Tools page getting displayed with all tools data")
            page = Paginator(tools_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = tools_Data.count()
            print("None Selected")
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'toolsdata': tools_Data,
                'tools_title': 'none',
                'toolscategory': toolsCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }

        return render(request, 'Localisation_App/tools.html', context)
    except:
        return render(request, "Localisation_App/serverdown.html")


   
def toolsReset(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        tools_Data = ToolsData.objects.all()   
        Tools_Category.objects.all().update(Tools_Cat_Status=False)
        toolsCategory_data = Tools_Category.objects.all() 
        count = ToolsData.objects.all().count()
        page = Paginator(tools_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = tools_Data.count()
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'toolsdata': tools_Data,
            'tools_title': 'none',
            'toolscategory': toolsCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count,
            'form': UserLoginForm()
        }
        logger.info("Tools page getting displayed")
        # if request.user.is_authenticated:
        #     return render(request, 'Localisation_App/tools.html', context)
        # else:
        return render(request, 'Localisation_App/tools.html', context)
    except:
        return render(request, "Localisation_App/serverdown.html")




def toolsDownloadCounter(request, id):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        print("requestid", id)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = ''
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        print("ip", ip)
        saved_ip = None
        time_posted = request.session.get('tools_Download_time')
        tools_obj = ToolsData.objects.get(pk=id)
        tools_requested_title = tools_obj.ToolsData_HeadingName
        Heading = request.session.get('toolsDownloadCounter_toolHeading')
        savedTimeInSession = None
        time_diff = 0
        logger.info("Inside Tools page, toolsDownloadCounter function checking where saved heading name and requested tools heading name is different or not")
        if tools_requested_title == Heading:
            logger.info("Inside Tools page, toolsDownloadCounter function, saved heading name and requested tools heading name is same")
            if time_posted is not None:
                logger.info("Tools page, time_posted is saved in tools_Download_time is not none ")
                savedTimeInSession = datetime.fromisoformat(time_posted[:-1])
                dataCurrentTime = datetime.now()
                print("time", type(dataCurrentTime))
                timediff = dataCurrentTime - savedTimeInSession
                time_diff = timediff.total_seconds()
                print("timediff", timediff.total_seconds())
                logger.info("Tools page, calculating time difference from saved time with first button click to current button click time")
            else:
                logger.info("Tools page, time_posted is saved in tools_Download_time is none ")
                print("time_posted none")
        else:
            logger.info( "Tools page, checking where saved heading name and requested name is different")
            time_diff = 500
        print("saved_ip", saved_ip)

        if time_diff < 300:
            logger.info("Tools page,if time diff. is less than 300 seconds, then it will save requested ip to toolsDownloadCounter_ip for creating session with ip")
            saved_ip = request.session.get('toolsDownloadCounter_ip')
        else:
            logger.info("Tools page,if time diff. is more than 300 seconds, then it will set none to toolsDownloadCounter_ip session for not creating session with ip")
            request.session['toolsDownloadCounter_ip'] = None

        if ip != saved_ip:
            logger.info("Tools page,it will check that within 300 second request is not comming from same ip, it will increase download count, and set toolsDownloadCounter_ip as requested ip and requested time to tools_Download_time ")
            # print("savedTimeInSession inside second not none")
            # if ip != saved_ip:
            print("ip is defferent inside second not none")
            # if time_diff < 10:
            print("time is less than 10 seconds inside second not none")
            request.session['toolsDownloadCounter_ip'] = ip
            data = datetime.now()
            print("time", type(data))
            data1 = json.dumps(data, default=json_util.default)
            aList = json.loads(data1)
            testdata = aList['$date']
            request.session['tools_Download_time'] = testdata
            print("increase download count second")
            tool_obj = ToolsData.objects.get(pk=id)
            print("tools_obje", tool_obj)
            print("before", tool_obj.ToolsData_DownloadCounter)
            tool_obj.ToolsData_DownloadCounter = tool_obj.ToolsData_DownloadCounter + 1
            tool_obj.save()
            datatotest=ToolsData.objects.get(pk=id)
            print("test here",datatotest.ToolsData_DownloadCounter)
            request.session['toolsDownloadCounter_toolHeading'] = tool_obj.ToolsData_HeadingName
            print("after", tool_obj.ToolsData_DownloadCounter)
            return redirect('Localisation_App:toolsReset')
        else:
            logger.info("Tools page,if within 300 second request is comming from same ip, it will not increase download count, and set toolsDownloadCounter_ip as requested ip and requested time to tools_Download_time ")
            print("ip is same inside second none")
            # request.session['toolsDownloadCounter_ip'] = ip
            tool_obj = ToolsData.objects.get(pk=id)
            # request.session['toolsDownloadCounter_toolHeading'] = tool_obj.ToolsData_HeadingName
            data = datetime.now()
            data1 = json.dumps(data, default=json_util.default)
            aList = json.loads(data1)
            testdata = aList['$date']
            # request.session['tools_Download_time'] = testdata
            print("inside second none")
            return redirect('Localisation_App:toolsReset')
    except:
        return render(request, "Localisation_App/serverdown.html")
       
 


# Resources Page

def resourcesPage(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        Resources_Category.objects.all().update(Resources_Cat_Status=False)
        if cache.get("All_resoucesCategory_data"):
            resoucesCategory_data = cache.get("All_resoucesCategory_data")
            print("cache data")
        else:
            resoucesCategory_data = Resources_Category.objects.all()
            cache.set("All_resoucesCategory_data", resoucesCategory_data)
            print("database data")
        
        if cache.get("All_resouces_data"):
            resources_Data = cache.get("All_resouces_data")
            print("cache data")
        else:
            resources_Data = ResourceData.objects.all()
            cache.set("All_resouces_data", resources_Data)
            print("database data")
        
        
        count = ResourceData.objects.all().count()
        page = Paginator(resources_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = resources_Data.count()
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'resoucesdata': resources_Data,
            'resource_title': 'none',
            'resourcescategory': resoucesCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count
        }
        logger.info("Resources page getting displayed")
        return render(request, 'Localisation_App/resources.html', context)
    except:
        return render(request, "Localisation_App/serverdown.html")
    


def resources(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        checklist1 = []
        category_name = []
        pagestatus = False
        filtered_Resources_Data = ResourceData.objects.none()
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        resoucesCategory_data = Resources_Category.objects.all()

        if cache.get("All_resources_data1"):
            resources_Data=cache.get("All_resources_data1")
            print("cache data")
        else:
            resources_Data = ResourceData.objects.all()
            cache.set("All_resources_data1",resources_Data)
            print("database data")
        
        count = ResourceData.objects.all().count()
        try:
            if request.method == "POST":
                # print("allcheched",request.POST.get('all_checkbox'))
                if request.POST.get('all_checkbox') != 'all_Checked':
                    category_name = []
                    q = ResourceData.objects.none()
                    print("dumydata", q)
                    checklist = request.POST.getlist('checkbox')
                    # print(checklist)
                    Resources_Category.objects.all().update(Resources_Cat_Status=False)
                    for n in checklist:
                        Resources_Category.objects.filter(
                            pk=int(n)).update(Resources_Cat_Status=True)
                    checklist.append(20202020220202020202)
                    if cache.get(checklist):
                        resourcesData_Checked=cache.get(checklist)
                        logger.info("Inside resources function, fetching Resources_Category data by selected category ids through cache")
                    else:
                        resourcesData_Checked = Resources_Category.objects.filter(
                        id__in=checklist)
                        cache.set(checklist,resourcesData_Checked)
                        logger.info("Inside resources function, fetching Resources_Category data by selected category ids through database") 
                    
                    for cat_Type in resourcesData_Checked:
                        category_name.append(cat_Type.Resources_CategoryType)
                    # print("list",category_name)
                    # print("tuple",tuple(category_name))
                    category_name.append("ToFetch_FilteredResources_With_Cache")
                    to_fetch = tuple(category_name)
                    if cache.get(to_fetch):
                        filtered_Resources_Data=cache.get(to_fetch)
                        logger.info("Inside resources function, fetching ResourceData data by selected category names through cache")
                    else:
                        for cat_name in to_fetch:
                            filtered_Resources_Data = filtered_Resources_Data | ResourceData.objects.filter(
                            ResourceData_CategoryType__Resources_CategoryType__contains=cat_name)
                        cache.set(to_fetch,filtered_Resources_Data)
                        logger.info("Inside resources function, fetching ResourceData data by selected category names through database")

                    count = filtered_Resources_Data.count()
                    page = Paginator(filtered_Resources_Data, 8)
                    page_list = request.GET.get('page')
                    # print("pagenumber",page_list)
                    page = page.get_page(page_list)
                    logger.info("Resources page getting displayed with selected category filteration")
                    context = {
                        'topmenus': top_menu_items_data,
                        'FooterMenuItemsdata': footer_menu_items_data,
                        'resoucesdata': filtered_Resources_Data,
                        'resource_title': 'none',
                        'resourcescategory': resoucesCategory_data,
                        "page": page,
                        'status_All_Checked': None,
                        'Pagination_Type': 'Category_Post',
                        'count': count
                    }
                    print("inside 1")

                    return render(request, 'Localisation_App/resources.html', context)
                else:
                    logger.info(
                        "Resources page getting displayed with all category filteration")
                    page = Paginator(resources_Data, 8)
                    Resources_Category.objects.all().update(Resources_Cat_Status=False)
                    page_list = request.GET.get('page')
                    page = page.get_page(page_list)
                    count = resources_Data.count()
                    context = {
                        'topmenus': top_menu_items_data,
                        'FooterMenuItemsdata': footer_menu_items_data,
                        'resoucesdata': resources_Data,
                        'resource_title': 'none',
                        'resourcescategory': resoucesCategory_data,
                        "page": page,
                        'status_All_Checked': 'True',
                        'Pagination_Type': 'All_Data',
                        'count': count
                    }
                    print("inside 2")
                    return render(request, 'Localisation_App/resources.html', context)
        except:
            print("Inside resources function, error in POST request for fetched category data")
            logger.error("Inside resources function, error in POST request for fetched category data")
            page = Paginator(resources_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = resources_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'resoucesdata': resources_Data,
                'resource_title': 'none',
                'resourcescategory': resoucesCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }

            return render(request, 'Localisation_App/resources.html', context)
        try:   
            for p in resoucesCategory_data:
                if p.Resources_Cat_Status == True:
                    print("true")
                    pagestatus = True
                    category_name.append(p.Resources_CategoryType)
            category_name.append("ToFetch_FilteredResources_With_Cache")
            to_fetch = tuple(category_name)
            if cache.get(to_fetch):
                filtered_Resources_Data=cache.get(to_fetch)
                logger.info("Inside resources function, fetching ResourceData data by selected category names through cache for pagination")
            else:
                for cat_name in to_fetch:
                    filtered_Resources_Data = filtered_Resources_Data | ResourceData.objects.filter(
                    ResourceData_CategoryType__Resources_CategoryType__contains=cat_name)
                cache.set(to_fetch,filtered_Resources_Data)
                logger.info("Inside resources function, fetching ResourceData data by selected category names through database for pagination")
            if pagestatus == True:
                logger.info(
                    "Resources page getting displayed with selected category filteration and pagination")
                page = Paginator(filtered_Resources_Data, 8)
                page_list = request.GET.get('page')
                page = page.get_page(page_list)
                count = filtered_Resources_Data.count()
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'resoucesdata': filtered_Resources_Data,
                    'resource_title': 'none',
                    'resourcescategory': resoucesCategory_data,
                    "page": page,
                    'status_All_Checked': None,
                    'Pagination_Type': 'Category_Post',
                    'count': count
                }

            else:
                logger.info(
                    "Resources page getting displayed with all category filteration and pagination")
                page = Paginator(resources_Data, 8)
                page_list = request.GET.get('page')
                page = page.get_page(page_list)
                count = resources_Data.count()
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'resoucesdata': resources_Data,
                    'resource_title': 'none',
                    'resourcescategory': resoucesCategory_data,
                    "page": page,
                    'status_All_Checked': 'True',
                    'Pagination_Type': 'All_Data',
                    'count': count
                }

            return render(request, 'Localisation_App/resources.html', context)
        except:
            logger.error("resources function, error in getting data with pagination request")
            page = Paginator(resources_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = resources_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'resoucesdata': resources_Data,
                'resource_title': 'none',
                'resourcescategory': resoucesCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
            return render(request, 'Localisation_App/resources.html', context)

    except:
        return render(request, "Localisation_App/serverdown.html")


def resourceSearch(request, resource_title):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        resource_searchData = resource_title.replace(" ", "-")
        print("titlenone", resource_title)
        print("replace space ", resource_title.replace(" ", "-"))

        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        if cache.get("All_resources_data1"):
            resources_Data=cache.get("All_resources_data1")
            print("cache data")
        else:
            resources_Data = ResourceData.objects.all()
            cache.set("All_resources_data1",resources_Data)
            print("database data")

        if cache.get("All_ResourceCat_Searcheddata"):
            resoucesCategory_data=cache.get("All_ResourceCat_Searcheddata")
            print("cache data")
        else:
            resoucesCategory_data = Resources_Category.objects.all()
            cache.set("All_ResourceCat_Searcheddata",resoucesCategory_data)
            print("database data")

        count = ResourceData.objects.all().count()
        try:
            if request.method == "POST":
                print("insideSearchMethod")
                print(resource_searchData)
                resource_searchData12 = request.POST.get("resourcename")
                print("resourcestitle", resource_searchData12)
                resource_searchData1 = resource_searchData12.replace(" ", "-")

                if resource_searchData1 != '':
                    resources_search=url+resource_searchData1
                    if cache.get(resources_search):
                        resource_Data=cache.get(resources_search)
                        logger.info("Inside resourceSearch function, fetching ResourceData data by searched name through cache")
                    else:
                        resource_Data = ResourceData.objects.filter(ResourceData_slug__icontains=resource_searchData1)
                        cache.set(resources_search,resource_Data)
                        logger.info("Inside resourceSearch function, fetching ResourceData data by searched name through database")

                    count = resource_Data.count()
                    print("dataresourcesdssds", count)
                    page = Paginator(resource_Data, 8)
                    page_list = request.GET.get('page')
                    # print("pagenumber",page_list)
                    page = page.get_page(page_list)
                    logger.info(
                        "Resources page getting displayed with searched data by slugs")
                    context = {
                        'topmenus': top_menu_items_data,
                        'FooterMenuItemsdata': footer_menu_items_data,
                        'resoucesdata': resource_Data,
                        'resource_title': resource_searchData1,
                        'resourcescategory': resoucesCategory_data,
                        "page": page,
                        'status_All_Checked': 'True',
                        'Pagination_Type': 'Searched_Post',
                        'count': count
                    }
                else:
                    logger.info("Resources page getting displayed with all data")
                    page = Paginator(resources_Data, 8)
                    page_list = request.GET.get('page')
                    page = page.get_page(page_list)
                    count = resources_Data.count()
                    context = {
                        'topmenus': top_menu_items_data,
                        'FooterMenuItemsdata': footer_menu_items_data,
                        'resoucesdata': resources_Data,
                        'resource_title': 'none',
                        'resourcescategory': resoucesCategory_data,
                        "page": page,
                        'status_All_Checked': 'True',
                        'Pagination_Type': 'Searched_Post',
                        'count': count
                    }
                return render(request, 'Localisation_App/resources.html', context)
        except:
            logger.info("resourceSearch function, error in POST request for fetcheing category data")
            page = Paginator(resources_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = resources_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'resoucesdata': resources_Data,
                'resource_title': 'none',
                'resourcescategory': resoucesCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }

            return render(request, 'Localisation_App/resources.html', context)
        
        try:
            if resource_searchData != 'none':
                logger.info(
                    "Resources page getting displayed with searched data by slugs with pagination")
                resources_search1=url+resource_searchData
                if cache.get(resources_search1):
                    resource_Data1=cache.get(resources_search1)
                    logger.info("Inside resourceSearch function, fetching ResourceData data by searched name through cache")
                else:
                    resource_Data1 = ResourceData.objects.filter(ResourceData_slug__icontains=resource_searchData)
                    cache.set(resources_search1,resource_Data1)
                    logger.info("Inside resourceSearch function, fetching ResourceData data by searched name through database")
                
                page = Paginator(resource_Data1, 8)
                page_list = request.GET.get('page')
                page = page.get_page(page_list)
                count = resource_Data1.count()
                print("hereee", resource_Data1)
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'resoucesdata': resource_Data1,
                    'resource_title': resource_searchData,
                    'resourcescategory': resoucesCategory_data,
                    "page": page,
                    'status_All_Checked': 'True',
                    'Pagination_Type': 'Searched_Post',
                    'count': count
                }
            else:
                logger.info("Resources page getting displayed with all data")
                page = Paginator(resources_Data, 8)
                page_list = request.GET.get('page')
                page = page.get_page(page_list)
                count = resources_Data.count()
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'resoucesdata': resources_Data,
                    'resource_title': 'none',
                    'resourcescategory': resoucesCategory_data,
                    "page": page,
                    'status_All_Checked': 'True',
                    'Pagination_Type': 'Searched_Post',
                    'count': count
                }

            return render(request, 'Localisation_App/resources.html', context)
        except:
            logger.info("resourceSearch function, error in getting data with pagination request")
            page = Paginator(resources_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = resources_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'resoucesdata': resources_Data,
                'resource_title': 'none',
                'resourcescategory': resoucesCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
            return render(request, 'Localisation_App/resources.html', context)

    except:
        return render(request, "Localisation_App/serverdown.html")


def resourcesReset(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        Resources_Category.objects.all().update(Resources_Cat_Status=False)
        resoucesCategory_data = Resources_Category.objects.all()
        resources_Data = ResourceData.objects.all()
        count = ResourceData.objects.all().count()
        page = Paginator(resources_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = resources_Data.count()
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'resoucesdata': resources_Data,
            'resource_title': 'none',
            'resourcescategory': resoucesCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count
        }
        logger.info("Resources page getting displayed")
        return render(request, 'Localisation_App/resources.html', context)
    except:
        return render(request, "Localisation_App/serverdown.html")


def resourceDownloadCounter(request, id):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        print("session time",)
        print("requestid", id)
        print("inside herehelloooooo")
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = ''
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        print("ip", ip)
        saved_ip = None
        time_posted = request.session.get('resources_Download_time')
        resources_obj = ResourceData.objects.get(pk=id)
        resource_requested_title = resources_obj.ResourceData_HeadingName
        Heading = request.session.get('resourcesDownloadCounter_resourceHeading')
        savedTimeInSession = None
        time_diff = 0
        logger.info("Inside Resources page, resourceDownloadCounter function checking where saved heading name and requested resources heading name is different or not")
        if resource_requested_title == Heading:
            logger.info("Inside Resources page, resourceDownloadCounter function, saved heading name and requested Resources heading name is same")
            if time_posted is not None:
                logger.info("Resources page, time_posted is saved in resources_Download_time is not none ")
                print("time_posted not none")
                print(time_posted)
                print("datatatataa", type(
                    datetime.fromisoformat(time_posted[:-1])))
                savedTimeInSession = datetime.fromisoformat(time_posted[:-1])
                dataCurrentTime = datetime.now()
                print("time", type(dataCurrentTime))
                timediff = dataCurrentTime - savedTimeInSession
                time_diff = timediff.total_seconds()
                print("timediff", timediff.total_seconds())
                logger.info("Resources page, calculating time difference from saved time with first button click to current button click time ")
            else:
                logger.info( "Resources page, time data is saved in resources_Download_time is none ")
                print("time_posted none")
        else:
            logger.info("Resources page,saved heading name and requested name is different")
            time_diff = 500
        print("saved_ip", saved_ip)

        if time_diff < 300:
            logger.info( "Resources page,if time diff. is less than 300 seconds, then it will save requested ip to resourcesDownloadCounter_ip for creating session ")
            saved_ip = request.session.get('resourcesDownloadCounter_ip')
        else:
            logger.info(
                "Resources page,if time diff. is more than 300 seconds, then it will set none to resourcesDownloadCounter_ip for not creating session ")
            request.session['resourcesDownloadCounter_ip'] = None

        if ip != saved_ip:
            logger.info("Resources page,within 300 second request is not comming from same ip , it will increase download count, and set resourcesDownloadCounter_ip as requested ip and requested time to resources_Download_time ")
            # print("savedTimeInSession inside second not none")
            # if ip != saved_ip:
            print("ip is defferent inside second not none")
            # if time_diff < 10:
            print("time is less than 10 seconds inside second not none")
            request.session['resourcesDownloadCounter_ip'] = ip
            data = datetime.now()
            print("time", type(data))
            data1 = json.dumps(data, default=json_util.default)
            aList = json.loads(data1)
            testdata = aList['$date']
            request.session['resources_Download_time'] = testdata
            print("increase download count second")
            resources_obj = ResourceData.objects.get(pk=id)
            print("resources_obje", resources_obj)
            print("before", resources_obj.ResourceData_DownloadCounter)
            resources_obj.ResourceData_DownloadCounter = resources_obj.ResourceData_DownloadCounter + 1
            resources_obj.save()

            request.session['resourcesDownloadCounter_resourceHeading'] = resources_obj.ResourceData_HeadingName
            print("after", resources_obj.ResourceData_DownloadCounter)
            return redirect('Localisation_App:resourcesReset')

        else:
            logger.info("Resources page,if within 300 second request is comming from same ip, it will not increase download count, and set resourcesDownloadCounter_ip as requested ip and requested time to resources_Download_time ")
            print("ip is same inside second none")
            # request.session['resourcesDownloadCounter_ip'] = ip
            resources_obj = ResourceData.objects.get(pk=id)
            # request.session['resourcesDownloadCounter_resourceHeading'] = resources_obj.ResourceData_HeadingName
            print("same and none ip first")
            data = datetime.now()
            print("time", type(data))
            data1 = json.dumps(data, default=json_util.default)
            aList = json.loads(data1)
            print("data343434", aList)
            testdata = aList['$date']
            # request.session['resources_Download_time'] = testdata
            print("inside second none")
            return redirect('Localisation_App:resourcesReset')
    except:
        return render(request, "Localisation_App/serverdown.html")


# Successstory Page

def successstoryPage(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        SuccessStories_Category.objects.update(SuccessStories_Cat_Status=False)
        if cache.get("All_SuccessStories_Category_data"):
            successStories_CategoryData = cache.get("All_SuccessStories_Category_data")
            print("cache data")
        else:
            successStories_CategoryData = SuccessStories_Category.objects.order_by(
            'SuccessStories_Cat_Priority')
            cache.set("All_SuccessStories_Category_data", successStories_CategoryData)
            print("database data")

        if cache.get("All_SuccessStories_data"):
            successStoriesData = cache.get("All_SuccessStories_data")
            print("cache data")
        else:
            successStoriesData = SuccessStories.objects.order_by(
            'SuccessStories_Priority')
            cache.set("All_SuccessStories_data", successStoriesData)
            print("database data")
    
        page = Paginator(successStoriesData, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = successStoriesData.count()
        logger.info("Success Stories page is getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'SuccessStoriesData': successStoriesData,
            'SuccessStories_CategoryData': successStories_CategoryData,
            'story_title': 'none',
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count
        }

        print("outside")
        return render(request, 'Localisation_App/successstory.html', context)
    except:
        return render(request, "Localisation_App/serverdown.html")


def successstory(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        checklist1 = []
        category_name = []
        pagestatus = False
        filtered_SuccessStories_Data = SuccessStories.objects.none()
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        if cache.get("All_successStories_data_data"):
            successStoriesData = cache.get("All_successStories_data_data")
            print("cache data")
        else:
            successStoriesData = SuccessStories.objects.all().order_by('SuccessStories_Priority')
            cache.set("All_successStories_data_data", successStoriesData)
            print("database data")
        # SuccessStrories_Category.objects.update(SuccessStrories_Cat_Status=False)
        successStories_CategoryData = SuccessStories_Category.objects.order_by(
            'SuccessStories_Cat_Priority')
        

        if request.method == "POST":
            # print("allcheched",request.POST.get('all_checkbox'))
            if request.POST.get('all_checkbox') != 'all_Checked':
                category_name = []
                filtered_SuccessStories_Data = SuccessStories.objects.none()
                # print("dumydata",q)
                checklist = request.POST.getlist('checkbox')
                # print(checklist)
                SuccessStories_Category.objects.all().update(SuccessStories_Cat_Status=False)
            
                for n in checklist:
                    SuccessStories_Category.objects.filter(
                        pk=int(n)).update(SuccessStories_Cat_Status=True)
                checklist.append(30303030330303030303)
                if cache.get(checklist):
                    successStoriesData_Checked=cache.get(checklist)
                    print("cache data")
                else:
                    successStoriesData_Checked = SuccessStories_Category.objects.filter(
                    id__in=checklist)
                    cache.set(checklist,successStoriesData_Checked)
                    print("database data") 
                
                for n in successStoriesData_Checked:
                    # print('hello',n.SuccessStrories_CategoryType)
                    category_name.append(n.SuccessStories_CategoryType)
                # print("list",category_name)
                # print("tuple",tuple(category_name))
                category_name.append("ToFetch_FilteredStories_With_Cache")
                to_fetch = tuple(category_name)
                if cache.get(to_fetch):
                    filtered_SuccessStories_Data=cache.get(to_fetch)
                    print("cache data")
                else:
                    for cat_name in to_fetch:
                        filtered_SuccessStories_Data = filtered_SuccessStories_Data | SuccessStories.objects.filter(
                        SuccessStories_category__SuccessStories_CategoryType__contains=cat_name).order_by('SuccessStories_category__SuccessStories_Cat_Priority', 'SuccessStories_Priority')
                # print("all data",q)
                    cache.set(to_fetch,filtered_SuccessStories_Data)
                    print("database data")

                
                count = filtered_SuccessStories_Data.count()
                print("hey", filtered_SuccessStories_Data)
                page = Paginator(filtered_SuccessStories_Data, 8)
                page_list = request.GET.get('page')
                # print("pagenumber",page_list)
                page = page.get_page(page_list)
                count = filtered_SuccessStories_Data.count()
                logger.info(
                    "Success stories page getting displayed with selected category filteration")
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'SuccessStoriesData': filtered_SuccessStories_Data,
                    'SuccessStories_CategoryData': successStories_CategoryData,
                    "page": page,
                    'story_title': 'none',
                    'Pagination_Type': 'Category_Post',
                    'status_All_Checked': None,
                    'count': count
                }
                print("inside 1")
                # return render(request,'Localisation_App/successstory.html',context)

            else:
                logger.info(
                    "Success stories page getting displayed with all category filteration")
                page = Paginator(successStoriesData, 8)
                SuccessStories_Category.objects.all().update(SuccessStories_Cat_Status=False)
                page_list = request.GET.get('page')
                page = page.get_page(page_list)
                count = successStoriesData.count()
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'SuccessStoriesData': successStoriesData,
                    'SuccessStories_CategoryData': successStories_CategoryData,
                    "page": page,
                    'story_title': 'none',
                    'status_All_Checked': 'True',
                    'Pagination_Type': 'All_Data',
                    'count': count
                }
                print("inside 2")

        for p in successStories_CategoryData:
            if p.SuccessStories_Cat_Status == True:
                print("true")
                pagestatus = True
                category_name.append(p.SuccessStories_CategoryType)
        category_name.append("ToFetch_FilteredStories_With_Cache")
        to_fetch = tuple(category_name)
        if cache.get(to_fetch):
            filtered_SuccessStories_Data=cache.get(to_fetch)
            print("cache data")
        else:
            for cat_name in to_fetch:
                filtered_SuccessStories_Data = filtered_SuccessStories_Data | SuccessStories.objects.filter(
                SuccessStories_category__SuccessStories_CategoryType__contains=cat_name).order_by('SuccessStories_category__SuccessStories_Cat_Priority', 'SuccessStories_Priority')
        
            cache.set(to_fetch,filtered_SuccessStories_Data)
            print("database data")

        if pagestatus == True:
            logger.info(
                "Success stories page getting displayed with selected category filteration and pagination")
            page = Paginator(filtered_SuccessStories_Data, 8)
            # SuccessStrories_Category.objects.all().update(SuccessStrories_Cat_Status=False)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = filtered_SuccessStories_Data.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'SuccessStoriesData': filtered_SuccessStories_Data,
                'story_title': 'none',
                'SuccessStories_CategoryData': successStories_CategoryData,
                "page": page,
                'Pagination_Type': 'Category_Post',
                'status_All_Checked': None,
                'count': count
            }

        else:
            logger.info(
                "Success stories page getting displayed with all category filteration and pagination")
            page = Paginator(successStoriesData, 8)
            # SuccessStrories_Category.objects.all().update(SuccessStrories_Cat_Status=False)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = successStoriesData.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'SuccessStoriesData': successStoriesData,
                'story_title': 'none',
                'SuccessStories_CategoryData': successStories_CategoryData,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }

        print("outside")
        return render(request, 'Localisation_App/successstory.html', context)
    except:
        return render(request, "Localisation_App/serverdown.html")


def successstorySearch(request, story_title):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        story_searchData = story_title.replace(" ", "-")
        print("titlenone", story_title)
        print("replace space ", story_title.replace(" ", "-"))
        print("titlenone", story_title)
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        successStories_CategoryData = SuccessStories_Category.objects.order_by(
            'SuccessStories_Cat_Priority')
        successStoriesData = SuccessStories.objects.all().order_by('SuccessStories_Priority')

        if request.method == "POST":
            print("insideSearchMethod")
            print(story_title)

            story_searchData12 = request.POST.get("storyname")
            print("successstoriestitle", story_searchData12)
            story_searchData1 = story_searchData12.replace(" ", "-")

            if story_searchData1 != '':
                stories_search=url+story_searchData1
                if cache.get(stories_search):
                    successStoriesData=cache.get(stories_search)
                    print("cache data")
                else:
                    successStoriesData = SuccessStories.objects.filter(
                    SuccessStories_slug__icontains=story_searchData1).order_by('SuccessStories_Priority')
                    cache.set(stories_search,successStoriesData)
                    print("database data")
                
                count = successStoriesData.count()
                print("dataStoriesdssds", count)
                page = Paginator(successStoriesData, 8)
                page_list = request.GET.get('page')
                # print("pagenumber",page_list)
                page = page.get_page(page_list)
                logger.info(
                    "Success stories page getting displayed with searched data by heading")
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'story_title': story_searchData1,
                    'SuccessStoriesData': successStoriesData,
                    'SuccessStories_CategoryData': successStories_CategoryData,
                    "page": page,
                    'status_All_Checked': 'True',
                    'Pagination_Type': 'Searched_Post',
                    'count': count
                }
            else:
                logger.info(
                    "Success stories  page getting displayed with all data")
                page = Paginator(successStoriesData, 8)
                page_list = request.GET.get('page')
                page = page.get_page(page_list)
                count = successStoriesData.count()
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'SuccessStoriesData': successStoriesData,
                    'story_title': 'none',
                    'SuccessStories_CategoryData': successStories_CategoryData,
                    "page": page,
                    'status_All_Checked': 'True',
                    'Pagination_Type': 'Searched_Post',
                    'count': count
                }
            return render(request, 'Localisation_App/successstory.html', context)
        if story_searchData != 'none':
            stories_search1=url+story_searchData
            if cache.get(stories_search1):
                Stories_Data1=cache.get(stories_search1)
                print("cache data")
            else:
                Stories_Data1 = SuccessStories.objects.filter(
                SuccessStories_slug__icontains=story_searchData).order_by('SuccessStories_Priority')
                cache.set(stories_search1,Stories_Data1)
                print("database data")


            
            page = Paginator(Stories_Data1, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = Stories_Data1.count()
            print("hereee", Stories_Data1)
            logger.info(
                "Success stories  page getting displayed with searched data by heading with pagination")
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'SuccessStoriesData': Stories_Data1,
                'story_title': story_searchData,
                'SuccessStories_CategoryData': successStories_CategoryData,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        else:
            logger.info("Success stories  page getting displayed with all data")
            page = Paginator(successStoriesData, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = successStoriesData.count()
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'SuccessStoriesData': successStoriesData,
                'story_title': 'none',
                'SuccessStories_CategoryData': successStories_CategoryData,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }

        return render(request, 'Localisation_App/successstory.html', context)
    except:
        return render(request, "Localisation_App/serverdown.html")


# Services Page

def services(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        tTS_Form = TTSservice()
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        if cache.get("All_servicesdata_data"):
            servicesdata = cache.get("All_servicesdata_data")
            print("cache data")
        else:
            servicesdata = Services.objects.all()
            cache.set("All_servicesdata_data", servicesdata)
            print("database data")
        
        logger.info("Services page getting displayed with all data")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'Servicesdata': servicesdata,
            'TTS_Form': tTS_Form,
        }
        return render(request, 'Localisation_App/services.html', context)
    except:
        logger.error("Error while, Displaying Services page with all data")
        return render(request, "Localisation_App/serverdown.html")


def srvEnableTyping(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        top_menu_items_data = TopMenuItems.objects.all()
        FooterMenuItemsdata = FooterMenuItems.objects.all()
        if request.method == "POST":
            nameodservice = request.POST.get("nameodservice")
            print("nameeee", nameodservice)

        return render(request, 'Localisation_App/ServicesDemoPage.html')
    except:
        return render(request, "Localisation_App/serverdown.html")


def srvGoTranslateWebLocalizer(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        logger.info("Go Translate WebLocalizer page getting displayed with all data")
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            "service": "goTranslate"
        }
        logger.info("srvGoTranslateWebLocalizer page displayed with all data")
        return render(request, 'Localisation_App/services_pages/gotranslate.html', context)
    except:
        logger.error("Error while, Displaying srvGoTranslateWebLocalizer page with all data")
        return render(request, "Localisation_App/serverdown.html")


def srvOnscreenKeyboard(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        if request.method == "POST":
            context = {
                "service": "onscreenkeyboard",
                "data": "onscreenkeyboard",
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
            }
            return render(request, 'Localisation_App/ServicesDemoPage.html', context)
        logger.info("On screen Keyboard page getting displayed with all data")
        context = {
            "service": "onscreenkeyboard",
            "data": "onscreenkeyboard",
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,

        }
        return render(request, 'Localisation_App/ServicesDemoPage.html', context)
    except:
        logger.error("Error while, Displaying srvOnscreenKeyboard page with all data")
        return render(request, "Localisation_App/serverdown.html")


def srvTTS(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        tTS_Form = TTSservice()
        if request.method == "POST":
            Details = TTSservice(request.POST)
            print("InsidePostMethod")
            if Details.is_valid():
                print('form is valid')
                language = request.POST.get("Select_Language_Pair")
                gender = request.POST.get("Gender")
                inputText = request.POST.get("InputText")
                print("Language", language)
                print("Gender", gender)
                print("InputText", inputText)

                url = 'http://localhost:8000/tts'
                payload = {'text': inputText, 'gender': gender, 'lang': language}
                logger.info("TTS APi getting called with form data")
                r = requests.post(url, data=payload)
                print('response', r)
                if r.status_code == 200:
                    logger.info(
                        "TTS ,Recieved success response, after APi called with form data")
                    data = r.json()
                    print('response', data)
                    print('file', data['outspeech_filepath'][0])
                    context = {
                        'Status': data['status'],
                        'outspeech_filepath': data['outspeech_filepath'][0],
                        "service": "srvTTS",
                        "TTS_Form": tTS_Form,
                        "data": "srvTTS",
                        'topmenus': top_menu_items_data,
                        'FooterMenuItemsdata': footer_menu_items_data,
                    }
                    logger.info(
                        "TTS Page getting displayed with recieved success response, after APi called with form data")
                    print("returned")
                    return render(request, 'Localisation_App/services_pages/ttsService.html', context)
        logger.info("TTS page getting displayed with all data")
        context = {
            "service": "srvTTS",
            "TTS_Form": tTS_Form,
            "data": "srvTTS",
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            "DIVTITLE": "HELLO"
        }
        return render(request, 'Localisation_App/services_pages/ttsService.html', context)
    except:
        logger.error("Error while, Displaying TTS page with all data")
        return render(request, "Localisation_App/serverdown.html")


def srvTransliteration(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        if request.method == "POST":
            context = {
                "service": "srvTransliteration",
                "data": "srvTransliteration",
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
            }
            return render(request, 'Localisation_App/ServicesDemoPage.html', context)
        logger.info("Transliteration page getting displayed")
        context = {
            "service": "srvTransliteration",
            "data": "srvTransliteration",
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,

        }
        return render(request, 'Localisation_App/services_pages/transliteration_modal.html', context)
    except:
        logger.error("Error while, Displaying Transliteration page with all data")
        return render(request, "Localisation_App/serverdown.html")


# Faqs Page
def faqs(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        if cache.get("All_Faqs_data"):
            faqs_data = cache.get("All_Faqs_data")
            print("cache data")
        else:
            faqs_data = FAQs.objects.all()
            cache.set("All_Faqs_data", faqs_data)
            print("database data")
        logger.info("Faqs page getting displayed")
        context = {
            'data': faqs_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'topmenus': top_menu_items_data,
            'faq_title': 'none'
        }
        return render(request, 'Localisation_App/faqs.html', context)
    except:
        logger.error("Error while, Displaying page page with all data")
        return render(request, "Localisation_App/serverdown.html")


def faqsSearch(request, faq_title):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        print("titlenone", faq_title)
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        faqs_data = FAQs.objects.all()
        count = faqs_data.count()
        if request.method == "POST":
            print("insideSearchMethod")
            print(faq_title)
            faq_title1 = request.POST.get("faq_title")
            print("faqtitle", faq_title1)

            if cache.get(faq_title1):
                fAQs_Data = cache.get(faq_title1)
                print("data", fAQs_Data)
                print("data from cache")
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'data': fAQs_Data,
                    'faq_title': faq_title1,
                    'count': count
                }
                return render(request, 'Localisation_App/faqs.html', context)
            else:
                if faq_title1 != '':
                    fAQs_Data = FAQs.objects.filter(
                        FAQs_Question__icontains=faq_title1)
                    count = fAQs_Data.count()
                    cache.set(faq_title1, fAQs_Data)
                    print("data from database")
                    logger.info("Faqs page getting displayed, with search filter")
                    context = {
                        'topmenus': top_menu_items_data,
                        'FooterMenuItemsdata': footer_menu_items_data,
                        'data': fAQs_Data,
                        'faq_title': faq_title1,
                        'count': count
                    }
                    return render(request, 'Localisation_App/faqs.html', context)
                else:
                    logger.info(
                        "Faqs page getting displayed, without search filter")
                    count = faqs_data.count()
                    context = {
                        'topmenus': top_menu_items_data,
                        'FooterMenuItemsdata': footer_menu_items_data,
                        'data': faqs_data,
                        'faq_title': 'none',
                        'count': count
                    }
                    return render(request, 'Localisation_App/faqs.html', context)

        return render(request, 'Localisation_App/faqs.html', context)
    except:
        logger.error("Error while, faqs search page page with all data")
        return render(request, "Localisation_App/serverdown.html")



# Terms And Conditions

def termsandcondition(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        if cache.get("All_TermsConditions_data_data"):
            footer_data = cache.get("All_TermsConditions_data_data")
            print("cache data")
        else:
            footer_data = Footer_Links.objects.get(Footer_Links_Title__contains='Terms & Conditions')
            cache.set("All_TermsConditions_data_data", footer_data)
            print("database data")
        
        print("hello", footer_data)
        logger.info("Terms and Condition page getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'content': footer_data

        }
        return render(request, 'Localisation_App/footer_links/termsandconditions.html', context)
    except:
        logger.error("Error while,Terms and Condition page page with all data")
        return render(request, "Localisation_App/serverdown.html")



# accessibility statement

def accessibilityStatement(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        if cache.get("All_AccessibilityStatement_data_data"):
            footer_data = cache.get("All_AccessibilityStatement_data_data")
            print("cache data")
        else:
            footer_data = Footer_Links.objects.get(
            Footer_Links_Title__contains='Accessibility Statement')
            cache.set("All_AccessibilityStatement_data_data", footer_data)
            print("database data")
        logger.info("accessibility_statement page getting displayed, with search filter")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'content': footer_data
        }
        return render(request, 'Localisation_App/footer_links/accessibility_statement.html', context)
    except:
        logger.error("Error while, accessibility_statement page page with all data")
        return render(request, "Localisation_App/serverdown.html")



# websitepolicies

def websitepolicy(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        if cache.get("All_WebsitePolicies_data_data"):
            footer_sub_data = cache.get("All_WebsitePolicies_data_data")
            print("cache data")
        else:
            footer_sub_data = Footer_Links_Info.objects.all().filter(
            Footer_Links_Info_MainTitle__Footer_Links_Title__contains="Website Policies")
            cache.set("All_WebsitePolicies_data_data", footer_sub_data)
            print("database data")

        if cache.get("All_Copyright_data"):
            content = cache.get("All_Copyright_data")
            print("cache data")
        else:
            content = Footer_Links_Info.objects.all().filter(
            Footer_Links_Info_SubTitle="Copyright Policy")[0]
            cache.set("All_Copyright_data", content)
            print("database data")

        
        
        print(content)
        logger.info("websitepolicy page getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'footer_sub_data': footer_sub_data,
            "content": content
        }
        return render(request, 'Localisation_App/footer_links/websitepolicies.html', context)
    except:
        logger.error("Error while, websitepolicy page page with all data")
        return render(request, "Localisation_App/serverdown.html")


# websitepolicies

def websitepolicydata(request, id):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        print("id : ", id)
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        # main_footer_data = Footer_Links.objects.all()

        if cache.get("All_WebsitePolicies_sub_data_data"):
            footer_sub_data = cache.get("All_WebsitePolicies_sub_data_data")
            print("cache data")
        else:
            footer_sub_data = Footer_Links_Info.objects.all().filter(
            Footer_Links_Info_MainTitle__Footer_Links_Title__contains="Website Policies")
            cache.set("All_WebsitePolicies_sub_data_data", footer_sub_data)
            print("database data")

        if cache.get("All_WebsitePolicies_sub_data_data"):
            footer_sub_data = cache.get("All_WebsitePolicies_sub_data_data")
            print("cache data")
        else:
            footer_sub_data = Footer_Links_Info.objects.all().filter(
            Footer_Links_Info_MainTitle__Footer_Links_Title__contains="Website Policies")
            cache.set("All_WebsitePolicies_sub_data_data", footer_sub_data)
            print("database data")
        
        content = Footer_Links_Info.objects.get(pk=id)
        logger.info("websitepolicy page getting displayed with selected subtitle")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'footer_sub_data': footer_sub_data,
            "content": content
        }
        return render(request, 'Localisation_App/footer_links/websitepolicies.html', context)
    except:
        logger.error("Error while, websitepolicy page with selected subtitle")
        return render(request, "Localisation_App/serverdown.html")



# Sitemap Page

def sitemap(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        if cache.get("All_Sitemap_data"):
            footer_data = cache.get("All_Sitemap_data")
            print("cache data")
        else:
            footer_data = Footer_Links.objects.get(
            Footer_Links_Title__contains='Sitemap')
            cache.set("All_Sitemap_data", footer_data)
            print("database data")
        
        logger.info("sitemap page getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'content': footer_data
        }
        return render(request, 'Localisation_App/footer_links/sitemap.html', context)
    except:
        logger.error("Error while, sitemap page with selected subtitle")
        return render(request, "Localisation_App/serverdown.html")



# Help Page

def helpData(request, id):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        print("id : ", id)
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        if cache.get("All_help_sub_data_data"):
            footer_sub_data = cache.get("All_help_sub_data_data")
            print("cache data")
        else:
            footer_sub_data = Footer_Links_Info.objects.all().filter(
            Footer_Links_Info_MainTitle__Footer_Links_Title__contains="help")
            cache.set("All_help_sub_data_data", footer_sub_data)
            print("database data")
        
        print("Help ", footer_sub_data)
        content = Footer_Links_Info.objects.get(pk=id)
        logger.info("Help page getting displayed with selected subtitle")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            "footer_sub_data": footer_sub_data,
            "content": content
        }
        return render(request, 'Localisation_App/footer_links/help.html', context)
    except:
        logger.error("Error while, help page with selected subtitle")
        return render(request, "Localisation_App/serverdown.html")



# help

def help(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        
        if cache.get("All_help_data"):
            footer_sub_data = cache.get("All_help_data")
            print("cache data")
        else:
            footer_sub_data = Footer_Links_Info.objects.all().filter(
            Footer_Links_Info_MainTitle__Footer_Links_Title__contains="help")
            cache.set("All_help_data", footer_sub_data)
            print("database data")

        if cache.get("All_Reader_data"):
            content = cache.get("All_Reader_data")
            print("cache data")
        else:
            content = Footer_Links_Info.objects.all().filter(
            Footer_Links_Info_SubTitle="Screen Reader Access")[0]
            cache.set("All_Reader_data", content)
            print("database data")
        
        print(content)
        logger.info("Help page getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            "footer_sub_data": footer_sub_data,
            "content": content
        }
        return render(request, 'Localisation_App/footer_links/help.html', context)
    except:
        logger.error("Error while, help page")
        return render(request, "Localisation_App/serverdown.html")


def contactus(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        logger.info("Contact us page getting displayed")
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        footer_sub_data = Footer_Links_Info.objects.all().filter(
            Footer_Links_Info_MainTitle__Footer_Links_Title__contains="help")

        num = random.randrange(1121, 9899)
        logger.info("random num generated for captcha in contact us page")
        str_num = str(num)
        context = {
            'FooterMenuItemsdata': footer_menu_items_data,
            'footer_sub_data': footer_sub_data,
            'topmenus': top_menu_items_data,
            'img': str_num
        }

        return render(request, 'Localisation_App/contactus.html', context)
    except:
        logger.error("Error while, random num generated for captcha in contact us page")
        return render(request, "Localisation_App/serverdown.html")


def submit(request, img):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if request.method == "POST":
            name = request.POST.get("name")
            captcha = request.POST.get("captcha")
            email = request.POST.get("email")
            contactNumber = request.POST.get("phone-number")
            option = request.POST.get("option")
            comment = request.POST.get("comment")
            print(name, email, contactNumber, option, comment)
            ins = Contact(name=name, email=email, phone=contactNumber,
                        option=option, comment=comment)
            ins.save()
            if img == captcha:

                res = send_mail(option, option+" Recieved",
                                "tanvip@cdac.in", [email, 'sshivam@cdac.in'])
                print("reponse form email", res)
                messages.add_message(request, messages.SUCCESS,
                                    'feedback submitted successfully')
                print(messages)
                return redirect('Localisation_App:contactus')
        #    return HttpResponse("form submitted successfully")
            else:
                messages.add_message(request, messages.ERROR,
                                    'Captcha does not matched')
                return redirect('Localisation_App:contactus')
        else:
            messages.add_message(request, messages.ERROR, 'Server error')
            return redirect('Localisation_App:contactus')
    except:
        logger.error("Error while, while submiting contact us page")
        return render(request, "Localisation_App/serverdown.html")


# User Register, Login, Logout, Profile, Forgot Password, Change Password

def Register_user(request):
    try:
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        form = RegisterForm()
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'form': form
        }

        if request.method == 'POST':
            logger.info("Inside register page after submit button click")
            form = RegisterForm(request.POST)
            if form.is_valid():
                logger.info(
                    "Inside register page , If form is valid all data saved into User model")
                form.save()
                print("Form Data")
                UserRegistration.objects.create(userregistration_email_field=form.cleaned_data.get(
                    'username'), userregistration_password=form.cleaned_data.get('password1'), userregistration_confirm_password=form.cleaned_data.get('password2'), userregistration_active_status=form.cleaned_data.get('check'))
                messages.success(request, 'Account creation successful')
                logger.info(
                    "Inside register page,If form is valid all data saved into UserRegistration model")
                return redirect('/')
            else:
                logger.info(
                    "Inside register page,If form is not valid, it will through error message")
                print('Form is not valid')
                messages.error(request, 'Error while processing your request')
                context = {
                    'topmenus': top_menu_items_data,
                    'FooterMenuItemsdata': footer_menu_items_data,
                    'form': form
                }
                return render(request, 'Localisation_App/user/register.html', context)
        logger.info("Register page getting displayed with register form")
        return render(request, 'Localisation_App/user/register.html', context)
    except:
        logger.error("Error while, displaying Register page")
        return render(request, "Localisation_App/serverdown.html")


def login_user(request):
    try:
        print("login", request.session.get('requested_url'))
        form = UserLoginForm()
        url = request.session.get('requested_url')
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        if request.method == 'POST':
            form = UserLoginForm(data=request.POST)
            print(request.POST.get('username'))
            print(request.POST.get('password'))
            if form.is_valid():
                print("loginform")
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                print("if form is valid")
                logger.info(
                    "Login user form , if form is valid, data is passed to authenticate function ")
                user = authenticate(username=username, password=password)
                if user is not None:
                    logger.info(
                        "Login user form, after successfull authentication, login() function called ")
                    print("second method called")
                    login(request, user)
                    if url != None:
                        return redirect('Localisation_App:'+url)
                    else:
                        return redirect('/')
                else:
                    logger.error(
                        "Login user form, Error in user login authentication")
                    messages.error(request, 'Wrong Email or Password')
                    return redirect('Localisation_App:login')

            else:
                logger.error(
                    "Login user form, Error Processing Your Request,Wrong Email or password ")
                messages.error(
                    request, 'Chcek your Email or Password')
                return redirect('Localisation_App:login')
        else:
            logger.info("Login user form page getting displayed ")
            context = {
                'topmenus': top_menu_items_data,
                'FooterMenuItemsdata': footer_menu_items_data,
                'form': UserLoginForm()
            }
            return render(request, 'Localisation_App/user/login.html', context)
    except:
        logger.error("Error while, displaying Login page")
        return render(request, "Localisation_App/serverdown.html")


def logout_user(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        print(url)
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        logger.error("Logout user")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,

        }
        logout(request)
        return render(request, 'Localisation_App/user/logout.html', context)
    except:
        logger.error("Error while, displaying Logout page")
        return render(request, "Localisation_App/serverdown.html")


def User_Profile(request, id):
    try:
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        print("id", id)
        user_obj = User.objects.get(pk=id)
        username = user_obj.username
        print("obje", user_obj.username)
        userRegister_obj = UserRegistration.objects.get(
            userregistration_email_field=username)
        print("obj454e", userRegister_obj.userregistration_email_field)

        context = {
            "User_obj": userRegister_obj,
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
        }
        return render(request, 'Localisation_App/user/profile.html', context)
    except:
        logger.error("Error while, displaying User Profile page")
        return render(request, "Localisation_App/serverdown.html")


def changePassword(request, token):
    try:
        form = UserChangePasswordForm()
        print("token", token)
        user_Profile_obj = UserRegistration.objects.get(
            userregistration_token=token)
        if user_Profile_obj is not None:
            print("inside change padsword", user_Profile_obj.pk)
            if request.method == 'POST':
                form = UserChangePasswordForm(data=request.POST)
                if form.is_valid():
                    print("inside Post")
                    password1 = form.cleaned_data['password1']
                    password2 = form.cleaned_data['password2']
                    user_id = request.POST.get('user_id')
                    logger.info("change password page, form is valid")
                    if password1 == password2:
                        logger.info(
                            "change password page, both passwors are matched")
                        if user_id is None:
                            logger.error("change password page, user_id not found")
                            messages.error(request, 'User Not Found')
                            return redirect('http://127.0.0.1:5555/changePassword/'+token)
                        else:
                            logger.info("change password page, user_id found")
                            user_Register_obj = UserRegistration.objects.get(
                                pk=user_id)
                            user_Register_obj.userregistration_password = password1
                            user_Register_obj.userregistration_confirm_password = password2
                            user_Register_obj.userregistration_confirm_password = password2
                            user_Register_obj.userregistration_token = None
                            user_Register_obj.save()
                            logger.info(
                                "change password page, updated password saved into user registration model")
                            user_main_obj = User.objects.get(
                                username=user_Profile_obj.userregistration_email_field)
                            user_main_obj.set_password(password1)
                            user_main_obj.save()
                            logger.info(
                                "change password page, updated password saved into user model")
                            logger.info(
                                "Password Reset Successfully, Token expired")
                            messages.success(
                                request, 'Password Reset Successfully')
                            print('Password Reset Successfully ')
                            return redirect('Localisation_App:login')
                    else:
                        logger.error("Passwords are not matching")
                        messages.error(request, 'Passwords are not matching')
                        return redirect('http://127.0.0.1:5552/changePassword/'+token)
                else:
                    logger.error("form is not valid")
                    messages.error(request, 'Data is not valid')
                    return redirect('http://127.0.0.1:5552/changePassword/'+token)
            else:
                user_id = user_Profile_obj.pk
                context = {
                    'form': form,
                    'User_Id': user_id
                }
                messages.error(request, '')
                return render(request, 'Localisation_App/user/changePassword.html', context)
        else:
            logger.error("change password page, user not found")
            messages.success(request, 'User Not Found')
            print('User Not Found')
            return redirect('http://127.0.0.1:5552/changePassword/'+token)
    except:
        logger.error("Error while, displaying Change Password page")
        return render(request, "Localisation_App/serverdown.html")


def forgetPassword(request):
    try:
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        form = UserForgetPasswordForm()
        try:
            if request.method == 'POST':
                form = UserForgetPasswordForm(data=request.POST)
                if form.is_valid():
                    logger.info("Forgot password page form is valid")
                    print('insideValidmethod')
                    username = form.cleaned_data['username']
                    if not User.objects.filter(username=username).first():
                        logger.error("No user found with this Email")
                        messages.error(
                            request, 'No user found with this Email')
                        print('No user found with this Email')
                        return redirect('Localisation_App:forgetPassword')
                    else:
                        logger.info(
                            "User found with this Email inside User model")
                        print('user is not none')
                        user_obj = User.objects.get(username=username)
                        print("userghjkj", user_obj)
                        token = str(uuid.uuid4())
                        # logger.info(
                        #     "Inside forgot password function, token is created")
                        logger.info(
                            "User found with this Email inside UserRegistration model")
                        print("username", username)
                        user_Profile_obj = UserRegistration.objects.get(
                            userregistration_email_field=username)
                        print("userrtyt", user_Profile_obj)
                        user_Profile_obj.userregistration_token = token
                        user_Profile_obj.save()
                        logger.info(
                            "Inside forgot password function, token is saved in UserRegistration model")

                        mail_send_status = send_forget_password_email(
                            user_Profile_obj.userregistration_email_field, token)
                        print("userdata", user_obj)

                        print("mail_send_status", mail_send_status)
                        if mail_send_status:
                            logger.info(
                                "Inside forgot password function, An email is sent on your registered Email-Id")
                            messages.success(
                                request, 'An email is sent on your registered Email-Id')
                            print('An email is sent')
                            return redirect('Localisation_App:forgetPassword')
                        else:
                            logger.error(
                                "Inside forgot password function, Failed to send sn email")
                            messages.error(request, 'Failed to send an email')
                            print('Failed to send sn email')
                            return redirect('Localisation_App:forgetPassword')
                else:
                    logger.error(
                        "Inside forgot password function, Form is not valid")
                    messages.error(request, 'Email is not valid')
                    return redirect('Localisation_App:forgetPassword')
        except Exception as e:
            print(e)
        logger.info("Forgot password page is getting displayed")
        messages.error(request, '')
        context = {
            'form': form,
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
        }
        return render(request, 'Localisation_App/user/forgetPassword.html', context)
    except:
        logger.error("Error while, displaying Forgot Password page")
        return render(request, "Localisation_App/serverdown.html")


def goTranslate(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        logger.info("goTranslate page is getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            "service": "goTranslate"

        }
        return render(request, 'Localisation_App/services_pages/gotranslate.html', context)
    except:
        logger.error("Error while, displaying goTranslate page")
        return render(request, "Localisation_App/serverdown.html")


# Dashboard 

def dashboard(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        if cache.get("Total_Tools_DownloadCount"):
            Total_Tools_DownloadCount = cache.get("Total_Tools_DownloadCount")
            print("cache data")
        else:
            Total_Tools_DownloadCount = ToolsData.objects.aggregate(
            Sum('ToolsData_DownloadCounter'))
            cache.set("Total_Tools_DownloadCount", Total_Tools_DownloadCount)
            print("database data")
        
        if cache.get("Total_ResourceData_DownloadCount"):
            Total_ResourceData_DownloadCount = cache.get("Total_ResourceData_DownloadCount")
            print("cache data")
        else:
            Total_ResourceData_DownloadCount = ResourceData.objects.aggregate(
            Sum('ResourceData_DownloadCounter'))
            cache.set("Total_ResourceData_DownloadCount", Total_ResourceData_DownloadCount)
            print("database data")

        SuccessStoriescategory_name = []
        countOfStoriesWithCategory = []
        if cache.get("All_SuccessStories_Category_dashboard"):
            successStories_CategoryData = cache.get("All_SuccessStories_Category_dashboard")
            print("cache data")
        else:
            successStories_CategoryData = SuccessStories_Category.objects.all()
            cache.set("All_SuccessStories_Category_dashboard", successStories_CategoryData)
            print("database data")


        toolscategory_name = []
        countOfToolsWithCategory = []
        if cache.get("All_tools_Category_dashboard"):
            toolsCategory_data = cache.get("All_tools_Category_dashboard")
            print("cache data")
        else:
            toolsCategory_data = Tools_Category.objects.all()
            cache.set("All_tools_Category_dashboard", toolsCategory_data)
            print("database data")
        

        resourcescategory_name = []
        countOfResourcesWithCategory = []
        if cache.get("All_Resources_Category_dashboard"):
            resourcesCategory_data = cache.get("All_Resources_Category_dashboard")
            print("cache data")
        else:
            resourcesCategory_data = Resources_Category.objects.all()
            cache.set("All_Resources_Category_dashboard", resourcesCategory_data)
            print("database data")
        

        toolsName = []
        id = []
        toolsName_hitCount_Per_Name = []
        if cache.get("All_tools_data_dashboard"):
            tools_data = cache.get("All_tools_data_dashboard")
            print("cache data")
        else:
            tools_data = ToolsData.objects.all()
            cache.set("All_tools_data_dashboard", tools_data)
            print("database data")

        resourcesName = []
        id_resources = []
        resourcesName_hitCount_Per_Name = []
        if cache.get("All_resources_data_dashboard"):
            resources_data = cache.get("All_resources_data_dashboard")
            print("cache data")
        else:
            resources_data = ResourceData.objects.all()
            cache.set("All_resources_data_dashboard", resources_data)
            print("database data")
        

        if cache.get("All_SuccessStoriesCat_name_dashboard_toDisplay"):
            SuccessStoriescategory_name = cache.get("All_SuccessStoriesCat_name_dashboard_toDisplay")
            print("cache data")
        else:
            for n in successStories_CategoryData:
                SuccessStoriescategory_name.append(n.SuccessStories_CategoryType)
            cache.set("All_SuccessStoriesCat_name_dashboard_toDisplay", SuccessStoriescategory_name)
            print("database data")
        
        if cache.get("All_SuccessStoriescount_dashboard_toDisplay"):
            countOfStoriesWithCategory = cache.get("All_SuccessStoriescount_dashboard_toDisplay")
            print("cache data")
        else:
            for n in successStories_CategoryData:
                count = SuccessStories.objects.filter(
                    SuccessStories_category__SuccessStories_CategoryType=n.SuccessStories_CategoryType).count()
                countOfStoriesWithCategory.append(count)
            logger.info("Dashboard page, calculated total stories per category")
            cache.set("All_SuccessStoriescount_dashboard_toDisplay", countOfStoriesWithCategory)
            print("database data")

        


        if cache.get("All_toolsCat_name_dashboard_toDisplay"):
            toolscategory_name = cache.get("All_toolsCat_name_dashboard_toDisplay")
            print("cache data")
        else:
            for n in toolsCategory_data:
                toolscategory_name.append(n.Tools_CategoryType)
            cache.set("All_toolsCat_name_dashboard_toDisplay", toolscategory_name)
            print("database data")
        
        if cache.get("All_Toolscount_dashboard_toDisplay"):
            countOfToolsWithCategory = cache.get("All_Toolscount_dashboard_toDisplay")
            print("cache data")
        else:
            for n in toolsCategory_data:
                count = ToolsData.objects.filter(
                    ToolsData_CategoryType__Tools_CategoryType=n.Tools_CategoryType).count()
                countOfToolsWithCategory.append(count)
            logger.info("Dashboard page, calculated total tools per category")
            cache.set("All_Toolscount_dashboard_toDisplay", countOfToolsWithCategory)
            print("database data")

        


        if cache.get("All_resourcesCat_name_dashboard_toDisplay"):
            resourcescategory_name = cache.get("All_resourcesCat_name_dashboard_toDisplay")
            print("cache data")
        else:
            for n in resourcesCategory_data:
                resourcescategory_name.append(n.Resources_CategoryType)
            cache.set("All_resourcesCat_name_dashboard_toDisplay", resourcescategory_name)
            print("database data")
        
        if cache.get("All_resourcescount_dashboard_toDisplay"):
            countOfResourcesWithCategory = cache.get("All_resourcescount_dashboard_toDisplay")
            print("cache data")
        else:
            for n in resourcesCategory_data:
                count = ResourceData.objects.filter(
                    ResourceData_CategoryType__Resources_CategoryType=n.Resources_CategoryType).count()
                countOfResourcesWithCategory.append(count)
            logger.info("Dashboard page, calculated resources per category")
            cache.set("All_resourcescount_dashboard_toDisplay", countOfResourcesWithCategory)
            print("database data")


        for n in tools_data:
            id.append(n.id)
        for n in id:
            # print(n)
            data = ToolsData.objects.values('ToolsData_DownloadCounter').get(id=n)
            # print(data)
            toolsName_hitCount_Per_Name.append(data["ToolsData_DownloadCounter"])
        for n in id:
            datname = ToolsData.objects.values('ToolsData_HeadingName').get(id=n)
            toolsName.append(datname["ToolsData_HeadingName"])
        logger.info("Dashboard page, calculated total download hit ratio per tool")

    
        for n in resources_data:
            id_resources.append(n.id)
        for n in id_resources:
            # print(n)
            data = ResourceData.objects.values(
                'ResourceData_DownloadCounter').get(id=n)
            # print(data)
            resourcesName_hitCount_Per_Name.append(
                data["ResourceData_DownloadCounter"])
        for n in id_resources:
            datname = ResourceData.objects.values(
                'ResourceData_HeadingName').get(id=n)
            resourcesName.append(datname["ResourceData_HeadingName"])
        logger.info("Dashboard page, calculated total download hit ratio per tool")

        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'name': 'Success Strories Dataset',
            'successStories_CategoryData': SuccessStoriescategory_name,
            'count_Of_Stories_PerCategory': countOfStoriesWithCategory,

            'tools_CategoryData': toolscategory_name,
            'count_Of_Tools_PerCategory': countOfToolsWithCategory,

            'resources_CategoryData': resourcescategory_name,
            'count_Of_Resources_PerCategory': countOfResourcesWithCategory,

            'toolshit_name': toolsName,
            'toolsHitCount': toolsName_hitCount_Per_Name,

            'resourcesshit_name': resourcesName,
            'resourcesHitCount': resourcesName_hitCount_Per_Name,
            'Total_Tools_DownloadCount': Total_Tools_DownloadCount,
            'Total_ResourceData_DownloadCount': Total_ResourceData_DownloadCount

        }
        return render(request, 'Localisation_App/dashboard.html', context)
    except:
        logger.error("Error while, displaying dashboard page")
        return render(request, "Localisation_App/serverdown.html")


# Translation Quote

@login_required()
def translation_quote(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
        }

        """ 
        OLD CODE STARTS HERE 
        """

        # if request.method == 'POST':
        #     url = request.POST.get('url')

        #     validate = URLValidator()
        #     try:
        #         validate(url)
        #         crawled_data = crawl_data(url)
        #         data = crawled_data
        #         if data["status"]:
        #             status,total_words, unique_words = data.values()

        #             print("total_words = ", total_words)
        #             print("unique_words = ", unique_words)

        #             context['total_words'] = total_words
        #         else:
        #             print(data["message"])
        #             context['error_message'] = data['message']

        #         return render(request, "Localisation_App/translation_quote/translation_quote.html", context)
        #     except ValidationError as e:
        #         context['error_message'] = e.message
        #         return render(request, "Localisation_App/translation_quote/translation_quote.html", context)

        # return render(request, "Localisation_App/translation_quote/translation_quote.html", context)

        """ 
        OLD CODE ENDS HERE
        
        """

        form = TranslationQuoteForm()
        context['form'] = form

        if request.method == 'POST':
            url = request.POST.get('url')
            company_email = request.POST.get('company_email')
            language = request.POST.get('language')
            domain = request.POST.get('domain')
            delivery_date = request.POST.get('delivery_date')
            client_remark = request.POST.get('client_remark')

            form = TranslationQuoteForm(request.POST)

            context['form'] = form

            #  validations
            validate_url = validators.URLValidator()
            validate_email = validators.EmailValidator()

            try:
                validate_url(url)

            except ValidationError as e:
                context['url_error'] = e.message
                return render(request, "Localisation_App/translation_quote/translation_quote.html", context)

            try:
                validate_email(company_email)
            except ValidationError as e:
                context['email_error'] = e.message
                return render(request, "Localisation_App/translation_quote/translation_quote.html", context)

            if form.is_valid():
                print("validation success")
                print(form.cleaned_data['url'])
                print(form.cleaned_data['company_email'])
                print(form.cleaned_data['language'])
                print(form.cleaned_data['domain'])
                print(form.cleaned_data['delivery_date'])
                print(form.cleaned_data['client_remark'])

                # add user
                current_user = request.user

                print(current_user)
                try:
                    date1 = form.cleaned_data['delivery_date']
                    if date1 < date.today():
                        raise ValidationError(
                            "Delivery date cannot be in the past!")
                except ValidationError as e:
                    context['date_error'] = e.message
                    return render(request, "Localisation_App/translation_quote/translation_quote.html", context)

                try:
                    if len(client_remark) > 5000:
                        raise ValidationError(
                            # "You have entered " + str(len(client_remark)) + " characters But only 5000 characters allowed"
                            "Max. Character Limit Exceeded(maximum length 5000 characters)"
                        )
                except ValidationError as e:
                    context['remark_error'] = e.message
                    return render(request, "Localisation_App/translation_quote/translation_quote.html", context)

                # generate application number (UNIQUE)
                #
                application_number = str('GI-' + str(date.today().year) + '-' +
                                        current_user.username[0:2].upper() + str(random.randrange(100000000, 1000000000)))

                data = TranslationQuote(
                    url=url, company_email=company_email, language=language, domain=domain, delivery_date=delivery_date, client_remark=client_remark, application_number=application_number, username=current_user)
                data.save()
                context['status'] = 'success'
                context['message'] = "Form submitted successfully"
                
                # email sent
                res = send_mail("Translation Quote", "Your request for translation quote with application No : " + application_number + " submitted ssuccessfully.","tanvip@cdac.in", [company_email])
                print("reponse form email", res)

                return render(request, 'Localisation_App/translation_quote/translation_quote.html', context)
            else:
                context['status'] = 'error'
                context['message'] = "Invalid URL!"

                # messages.error(request, 'Error Processing Your Request')

                return render(request, 'Localisation_App/translation_quote/translation_quote.html', context)

        return render(request, "Localisation_App/translation_quote/translation_quote.html", context)
    except:
        logger.error("Error while, displaying translation_quote page")
        return render(request, "Localisation_App/serverdown.html")



def machine_translation(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        logger.info("Machine Translation page is getting displayed")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data

        }

        return render(request, 'Localisation_App/services_pages/machine_translation.html', context)
    except:
        logger.error("Error while, displaying machine_translation page")
        return render(request, "Localisation_App/serverdown.html")


def name_matcher(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
        }

        return render(request, 'Localisation_App/services_pages/name_matcher.html', context)
    except:
        logger.error("Error while, displaying name_matcher page")
        return render(request, "Localisation_App/serverdown.html")


def empanelled_agencies(request):
    try:
        url = resolve(request.path_info).url_name
        request.session['requested_url'] = url
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        empanelled_agecies_data = EmpanelledAgencies.objects.all()
        empanelled_agecies_data_list = []
        for i in empanelled_agecies_data:
            data = {}
            data['company_name'] = i.company_name
            data['contact_person'] = i.contact_person

            emails = []
            for i in EmpanelledAgenciesEmail.objects.filter(empanelled_agencies=i):
                emails.append(i.email)
            data['email'] = emails

            empanelled_agecies_data_list.append(data)

        print(empanelled_agecies_data_list)

        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'empanelled_agencies_data': empanelled_agecies_data_list,
        }
        return render(request, 'Localisation_App/footer_links/empanelled_agencies.html', context)
    except:
        logger.error("Error while, displaying empanelled_agencies page")
        return render(request, "Localisation_App/serverdown.html")


# translation_quote_user_dashboard
@login_required
def translation_quote_user_dashboard(request):
    try:
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        current_user = request.user
        print(current_user)

        translation_quote_data = TranslationQuote.objects.filter(
            username=current_user)

        print(translation_quote_data)

        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'translation_quote_data': translation_quote_data,
        }
        return render(request, 'Localisation_App/translation_quote/translation_quote_user_dashboard.html', context)
    except:
        logger.error("Error while, displaying translation_quote_user_dashboard page")
        return render(request, "Localisation_App/serverdown.html")


# translation_quote_show
@login_required
def translation_quote_show(request, application_number):
    try:
        # print("application number ", application_number)
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        if cache.get(application_number):
            translation_quote_data = cache.get(application_number)
            print("cache data")
        else:
            translation_quote_data = TranslationQuote.objects.filter(
                application_number=application_number)[0]
            cache.set(application_number, translation_quote_data)
            print("database data")

        

        print(translation_quote_data)
        username = translation_quote_data.username
        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
            'translation_quote_data': translation_quote_data,
        }

        print("Email ", username.username)

        if username.username == 'admin':
            print("hii")
            return render(request, 'Localisation_App/translation_quote/translation_quote/translation_quote_show.html', context)
        else:
            user_details = UserRegistration.objects.filter(
                userregistration_email_field=username.username)[0]

            context['user_details'] = user_details
            return render(request, 'Localisation_App/translation_quote/translation_quote/translation_quote_show.html', context)
    except:
        logger.error("Error while, displaying translation_quote_show page")
        return render(request, "Localisation_App/serverdown.html")


def bhashini(request):
    try:
        if cache.get("All_top_menu_items_data_data"):
            top_menu_items_data = cache.get("All_top_menu_items_data_data")
            print("cache data")
        else:
            top_menu_items_data = TopMenuItems.objects.all()
            cache.set("All_top_menu_items_data_data", top_menu_items_data)
            print("database data")

        if cache.get("All_footer_menu_items_data_data"):
            footer_menu_items_data = cache.get("All_footer_menu_items_data_data")
            print("cache data")
        else:
            footer_menu_items_data = FooterMenuItems.objects.all()
            cache.set("All_footer_menu_items_data_data", footer_menu_items_data)
            print("database data")

        context = {
            'topmenus': top_menu_items_data,
            'FooterMenuItemsdata': footer_menu_items_data,
        }
        return render(request,'Localisation_App/bhashini.html',context)
    except:
        logger.error("Error while, displaying bhashini page")
        return render(request, "Localisation_App/serverdown.html")

def anuvaad(request):
    try:
        return render(request,'Localisation_App/services_pages/anuvaad.html')
    except:
        logger.error("Error while, displaying anuvaad page")
        return render(request, "Localisation_App/serverdown.html")
    