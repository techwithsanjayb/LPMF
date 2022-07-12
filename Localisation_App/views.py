
import re
from .forms import TTSservice, RegisterForm, TranslationQuoteForm, UserLoginForm,UserChangePasswordForm,UserForgetPasswordForm
from django.contrib import messages
from django.core.mail import send_mail, mail_admins
from django.core.paginator import Paginator
from multiprocessing import context
from django.contrib.auth import login, authenticate, logout,  update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.shortcuts import render, redirect
from .models import Article, SuccessStories, ResourceData, FAQs, NewsAndEvents, Services, ToolsData, TopMenuItems, SuccessStories_Category, Footer_Links, Footer_Links_Info, ToolsData, Tools_Category, FooterMenuItems, Tools_Searched_Title, Resources_Category, Contact, TranslationQuote, UserRegistration, GuidelinceForIndianGovWebsite
import random
import requests
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .word_count import crawl_data
from django.contrib.auth.models import User
import uuid
from .helpers import send_forget_password_email

global str_num
# Menu


def topmenu(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    context = {
        'topmenus': TopMenuItemsdata
    }
    return render(request, 'Localisation_App/base.html', context)

# Test Page


def Test(request):
    mail_admins('Test Mail', 'Test', 'sgpltr@gmail.com',
                'shubhiasati95@gmail.com')

    return render(request, 'Localisation_App/test.html')

# Home Page


def Home(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    articleData = Article.objects.all()
    successStoriesData = SuccessStories.objects.all()
    servicesdata = Services.objects.all()
    newsAndEventsData = NewsAndEvents.objects.all()

    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'ArticleData': articleData,
        'SuccessStoriesData': successStoriesData,
        'NewsAndEventsData': newsAndEventsData,
        'Servicesdata': servicesdata
    }
    return render(request, 'Localisation_App/home.html', context)

# About Us Page


def aboutus(request):
    print("hello")
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    articleData = Article.objects.all().filter(Article_HeadingName="About Us")
    print("TEst ", articleData)
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'ArticleData': articleData,
    }
    return render(request, 'Localisation_App/aboutus.html', context)

# Tools Page


def toolsPage(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    tools_Data = ToolsData.objects.all()
    Tools_Category.objects.all().update(Tools_Cat_Status=False)
    toolsCategory_data = Tools_Category.objects.all()
    count = ToolsData.objects.all().count()
    page = Paginator(tools_Data, 8)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    count = tools_Data.count()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'toolsdata': tools_Data,
        'tools_title': 'none',
        'toolscategory': toolsCategory_data,
        "page": page,
        'status_All_Checked': 'True',
        'Pagination_Type': 'All_Data',
        'count': count,
        'form': UserLoginForm()
    }
    return render(request, 'Localisation_App/tools.html', context)
    


def tools(request):
    checklist1 = []
    category_name = []
    pagestatus = False
    q = ToolsData.objects.none()
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    toolsCategory_data = Tools_Category.objects.all()
    tools_Data = ToolsData.objects.all()
    count = ToolsData.objects.all().count()

    if request.method == "POST":
        # print("allcheched",request.POST.get('all_checkbox'))
        if request.POST.get('all_checkbox') != 'all_Checked':
            category_name = []
            q = ToolsData.objects.none()
            print("dumydata", q)
            checklist = request.POST.getlist('checkbox')
            # print(checklist)
            Tools_Category.objects.all().update(Tools_Cat_Status=False)
            for n in checklist:
                Tools_Category.objects.filter(
                    pk=int(n)).update(Tools_Cat_Status=True)
            toolsData_Checked = Tools_Category.objects.filter(id__in=checklist)
            for n in toolsData_Checked:
                # print('hello',n.Tools_CategoryType)
                category_name.append(n.Tools_CategoryType)
            # print("list",category_name)
            # print("tuple",tuple(category_name))
            to_fetch = tuple(category_name)

            for c in to_fetch:
                # print(c)
                q = q | ToolsData.objects.filter(
                    ToolsData_CategoryType__Tools_CategoryType__contains=c)
            # print("all data",q)
            count = q.count()
            page = Paginator(q, 8)
            page_list = request.GET.get('page')
            # print("pagenumber",page_list)
            page = page.get_page(page_list)

            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'toolsdata': q,
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
            page = Paginator(tools_Data, 8)
            Tools_Category.objects.all().update(Tools_Cat_Status=False)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = ToolsData.objects.all().count()
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
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
    for p in toolsCategory_data:
        if p.Tools_Cat_Status == True:
            print("true")
            pagestatus = True
            category_name.append(p.Tools_CategoryType)
    to_fetch = tuple(category_name)
    for c in to_fetch:
        q = q | ToolsData.objects.filter(
            ToolsData_CategoryType__Tools_CategoryType__contains=c)
    print(q)

    if pagestatus == True:
        page = Paginator(q, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = q.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'toolsdata': q,
            'tools_title': 'none',
            'toolscategory': toolsCategory_data,
            "page": page,
            'status_All_Checked': None,
            'Pagination_Type': 'Category_Post',
            'count': count
        }

    else:
        page = Paginator(tools_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = tools_Data.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
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


def toolsSearch(request, tools_title):
    print("titlenone", tools_title)
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    toolsCategory_data = Tools_Category.objects.all()
    tools_Data = ToolsData.objects.all()

    if request.method == "POST":
        print("insideSearchMethod")
        print(tools_title)
        tools_title1 = request.POST.get("toolname")
        print("toolstitile", tools_title1)

        if tools_title1 != '':
            tools_Data = ToolsData.objects.filter(
                ToolsData_HeadingName__icontains=tools_title1)
            count = tools_Data.count()
            print("datatooldssds", count)
            page = Paginator(tools_Data, 8)
            page_list = request.GET.get('page')
            # print("pagenumber",page_list)
            page = page.get_page(page_list)
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'toolsdata': tools_Data,
                'tools_title': tools_title1,
                'toolscategory': toolsCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        else:
            page = Paginator(tools_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = tools_Data.count()
            print("None Selected")
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'toolsdata': tools_Data,
                'tools_title': 'none',
                'toolscategory': toolsCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        return render(request, 'Localisation_App/tools.html', context)
    if tools_title != 'none':
        tools_Data1 = ToolsData.objects.filter(
            ToolsData_HeadingName__icontains=tools_title)
        page = Paginator(tools_Data1, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = tools_Data1.count()
        print("hereee", tools_Data1)
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'toolsdata': tools_Data1,
            'tools_title': tools_title,
            'toolscategory': toolsCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    else:
        page = Paginator(tools_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = tools_Data.count()
        print("None Selected")
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'toolsdata': tools_Data,
            'tools_title': 'none',
            'toolscategory': toolsCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }

    return render(request, 'Localisation_App/tools.html', context)


def toolsReset(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    tools_Data = ToolsData.objects.all()
    Tools_Category.objects.all().update(Tools_Cat_Status=False)
    toolsCategory_data = Tools_Category.objects.all()
    count = ToolsData.objects.all().count()
    page = Paginator(tools_Data, 8)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    count = tools_Data.count()
    if request.method == "POST":
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'toolsdata': tools_Data,
            'tools_title': 'none',
            'toolscategory': toolsCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count
        }
        return render(request, 'Localisation_App/tools.html', context)


# Resources Page


def resourcesPage(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    resoucesCategory_data = Resources_Category.objects.all()
    resources_Data = ResourceData.objects.all()
    Resources_Category.objects.all().update(Resources_Cat_Status=False)
    count = ResourceData.objects.all().count()
    page = Paginator(resources_Data, 8)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    count = resources_Data.count()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'resoucesdata': resources_Data,
        'resource_title': 'none',
        'resourcescategory': resoucesCategory_data,
        "page": page,
        'status_All_Checked': 'True',
        'Pagination_Type': 'All_Data',
        'count': count
    }
    return render(request, 'Localisation_App/resources.html', context)


def resources(request):
    checklist1 = []
    category_name = []
    pagestatus = False
    q = ResourceData.objects.none()
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    resoucesCategory_data = Resources_Category.objects.all()
    resources_Data = ResourceData.objects.all()
    count = ResourceData.objects.all().count()

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
            resourcesData_Checked = Resources_Category.objects.filter(
                id__in=checklist)
            for n in resourcesData_Checked:
                category_name.append(n.Resources_CategoryType)
            # print("list",category_name)
            # print("tuple",tuple(category_name))
            to_fetch = tuple(category_name)

            for c in to_fetch:
                # print(c)
                q = q | ResourceData.objects.filter(
                    ResourceData_CategoryType__Resources_CategoryType__contains=c)
            # print("all data",q)
            count = q.count()
            page = Paginator(q, 8)
            page_list = request.GET.get('page')
            # print("pagenumber",page_list)
            page = page.get_page(page_list)

            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'resoucesdata': q,
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
            page = Paginator(resources_Data, 8)
            Resources_Category.objects.all().update(Resources_Cat_Status=False)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = resources_Data.count()
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
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
    for p in resoucesCategory_data:
        if p.Resources_Cat_Status == True:
            print("true")
            pagestatus = True
            category_name.append(p.Resources_CategoryType)
    to_fetch = tuple(category_name)
    for c in to_fetch:
        q = q | ResourceData.objects.filter(
            ResourceData_CategoryType__Resources_CategoryType__contains=c)
    print(q)

    if pagestatus == True:
        page = Paginator(q, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = q.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'resoucesdata': q,
            'resource_title': 'none',
            'resourcescategory': resoucesCategory_data,
            "page": page,
            'status_All_Checked': None,
            'Pagination_Type': 'Category_Post',
            'count': count
        }

    else:
        page = Paginator(resources_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = resources_Data.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'resoucesdata': resources_Data,
            'resource_title': 'none',
            'resourcescategory': resoucesCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count
        }

    return render(request, 'Localisation_App/resources.html', context)


def resourceSearch(request, resource_title):
    print("titlenone", resource_title)
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    resoucesCategory_data = Resources_Category.objects.all()
    resources_Data = ResourceData.objects.all()
    count = ResourceData.objects.all().count()

    if request.method == "POST":
        print("insideSearchMethod")
        print(resource_title)
        resource_title1 = request.POST.get("resourcename")
        print("resourcestitle", resource_title1)

        if resource_title1 != '':
            resource_Data = ResourceData.objects.filter(
                ResourceData_HeadingName__icontains=resource_title1)
            count = resource_Data.count()
            print("dataresourcesdssds", count)
            page = Paginator(resource_Data, 8)
            page_list = request.GET.get('page')
            # print("pagenumber",page_list)
            page = page.get_page(page_list)
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'resoucesdata': resource_Data,
                'resource_title': resource_title1,
                'resourcescategory': resoucesCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        else:
            page = Paginator(resources_Data, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = resources_Data.count()
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'resoucesdata': resources_Data,
                'resource_title': 'none',
                'resourcescategory': resoucesCategory_data,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        return render(request, 'Localisation_App/resources.html', context)
    if resource_title != 'none':
        resource_Data1 = ResourceData.objects.filter(
            ResourceData_HeadingName__icontains=resource_title)
        page = Paginator(resource_Data1, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = resource_Data1.count()
        print("hereee", resource_Data1)
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'resoucesdata': resource_Data1,
            'resource_title': resource_title,
            'resourcescategory': resoucesCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    else:
        page = Paginator(resources_Data, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = resources_Data.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'resoucesdata': resources_Data,
            'resource_title': 'none',
            'resourcescategory': resoucesCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }

    return render(request, 'Localisation_App/resources.html', context)


def resourcesReset(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    resources_Data = ResourceData.objects.all()
    Resources_Category.objects.all().update(Resources_Cat_Status=False)
    resoucesCategory_data = Resources_Category.objects.all()
    count = ResourceData.objects.all().count()
    page = Paginator(resources_Data, 8)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    count = resources_Data.count()
    if request.method == "POST":
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'resoucesdata': resources_Data,
            'resource_title': 'none',
            'resourcescategory': resoucesCategory_data,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count
        }
        return render(request, 'Localisation_App/resources.html', context)


# Successstory Page
def successstoryPage(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    SuccessStories_Category.objects.update(SuccessStories_Cat_Status=False)
    successStories_CategoryData = SuccessStories_Category.objects.order_by(
        'SuccessStories_Cat_Priority')
    successStoriesData = SuccessStories.objects.order_by(
        'SuccessStories_Priority')
    page = Paginator(successStoriesData, 8)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    count = successStoriesData.count()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
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


def successstory(request):
    checklist1 = []
    category_name = []
    pagestatus = False
    q = SuccessStories.objects.none()
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    # SuccessStrories_Category.objects.update(SuccessStrories_Cat_Status=False)
    successStories_CategoryData = SuccessStories_Category.objects.order_by(
        'SuccessStories_Cat_Priority')
    successStoriesData = SuccessStories.objects.all().order_by('SuccessStories_Priority')

    if request.method == "POST":
        # print("allcheched",request.POST.get('all_checkbox'))
        if request.POST.get('all_checkbox') != 'all_Checked':
            category_name = []
            q = SuccessStories.objects.none()
            # print("dumydata",q)
            checklist = request.POST.getlist('checkbox')
            # print(checklist)
            SuccessStories_Category.objects.all().update(SuccessStories_Cat_Status=False)
            for n in checklist:
                SuccessStories_Category.objects.filter(
                    pk=int(n)).update(SuccessStories_Cat_Status=True)
            successStoriesData_Checked = SuccessStories_Category.objects.filter(
                id__in=checklist)
            for n in successStoriesData_Checked:
                # print('hello',n.SuccessStrories_CategoryType)
                category_name.append(n.SuccessStories_CategoryType)
            # print("list",category_name)
            # print("tuple",tuple(category_name))
            to_fetch = tuple(category_name)

            for c in to_fetch:
                # print(c)
                q = q | SuccessStories.objects.filter(
                    SuccessStories_category__SuccessStories_CategoryType__contains=c).order_by('SuccessStories_category__SuccessStories_Cat_Priority', 'SuccessStories_Priority')
            # print("all data",q)
            count = q.count()
            print("hey", q)
            page = Paginator(q, 8)
            page_list = request.GET.get('page')
            # print("pagenumber",page_list)
            page = page.get_page(page_list)
            count = q.count()

            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'SuccessStoriesData': q,
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
            page = Paginator(successStoriesData, 8)
            SuccessStories_Category.objects.all().update(SuccessStories_Cat_Status=False)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = successStoriesData.count()
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
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
    to_fetch = tuple(category_name)
    for c in to_fetch:
        q = q | SuccessStories.objects.filter(
            SuccessStories_category__SuccessStories_CategoryType__contains=c).order_by('SuccessStories_category__SuccessStories_Cat_Priority', 'SuccessStories_Priority')
    print(q)

    if pagestatus == True:
        page = Paginator(q, 8)
        # SuccessStrories_Category.objects.all().update(SuccessStrories_Cat_Status=False)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = q.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'SuccessStoriesData': q,
            'story_title': 'none',
            'SuccessStories_CategoryData': successStories_CategoryData,
            "page": page,
            'Pagination_Type': 'Category_Post',
            'status_All_Checked': None,
            'count': count
        }

    else:
        page = Paginator(successStoriesData, 8)
        # SuccessStrories_Category.objects.all().update(SuccessStrories_Cat_Status=False)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = successStoriesData.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
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


def successstorySearch(request, story_title):
    print("titlenone", story_title)
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    successStories_CategoryData = SuccessStories_Category.objects.order_by(
        'SuccessStories_Cat_Priority')
    successStoriesData = SuccessStories.objects.all().order_by('SuccessStories_Priority')

    if request.method == "POST":
        print("insideSearchMethod")
        print(story_title)
        strory_title1 = request.POST.get("storyname")
        print("strory_title1", strory_title1)

        if strory_title1 != '':
            successStoriesData = SuccessStories.objects.filter(
                SuccessStories_TitleName__icontains=strory_title1).order_by('SuccessStories_Priority')
            count = successStoriesData.count()
            print("dataStoriesdssds", count)
            page = Paginator(successStoriesData, 8)
            page_list = request.GET.get('page')
            # print("pagenumber",page_list)
            page = page.get_page(page_list)
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'story_title': strory_title1,
                'SuccessStoriesData': successStoriesData,
                'SuccessStories_CategoryData': successStories_CategoryData,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        else:
            page = Paginator(successStoriesData, 8)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = successStoriesData.count()
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'SuccessStoriesData': successStoriesData,
                'story_title': 'none',
                'SuccessStories_CategoryData': successStories_CategoryData,
                "page": page,
                'status_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        return render(request, 'Localisation_App/successstory.html', context)
    if story_title != 'none':
        Stories_Data1 = SuccessStories.objects.filter(
            SuccessStories_TitleName__icontains=story_title).order_by('SuccessStories_Priority')
        page = Paginator(Stories_Data1, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = Stories_Data1.count()
        print("hereee", Stories_Data1)
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'SuccessStoriesData': Stories_Data1,
            'story_title': story_title,
            'SuccessStories_CategoryData': successStories_CategoryData,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    else:
        page = Paginator(successStoriesData, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = successStoriesData.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'SuccessStoriesData': successStoriesData,
            'story_title': 'none',
            'SuccessStories_CategoryData': successStories_CategoryData,
            "page": page,
            'status_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }

    return render(request, 'Localisation_App/successstory.html', context)


def successstoryReset(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    SuccessStories_Category.objects.update(SuccessStories_Cat_Status=False)
    successStories_CategoryData = SuccessStories_Category.objects.order_by(
        'SuccessStories_Cat_Priority')
    successStoriesData = SuccessStories.objects.all().order_by('SuccessStories_Priority')
    page = Paginator(successStoriesData, 8)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    count = successStoriesData.count()
    if request.method == "POST":
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
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


# Services Page
def services(request):
    tTS_Form = TTSservice()
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    servicesdata = Services.objects.all()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'Servicesdata': servicesdata,
        'TTS_Form': tTS_Form,
    }
    return render(request, 'Localisation_App/services.html', context)


def ServicesDemoPage(request):
    tTS_Form = TTSservice()
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        "service": "srvTTS",
        'TTS_Form': tTS_Form
    }
    return render(request, 'Localisation_App/ServicesDemoPage.html', context)


def srvEnableTyping(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    if request.method == "POST":
        nameodservice = request.POST.get("nameodservice")
        print("nameeee", nameodservice)

    return render(request, 'Localisation_App/ServicesDemoPage.html')


def srvGoTranslateWebLocalizer(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    return render(request, 'Localisation_App/ServicesDemoPage.html')


def srvOnscreenKeyboard(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    if request.method == "POST":
        context = {
            "service": "onscreenkeyboard",
            "data": "onscreenkeyboard",
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
        }
        return render(request, 'Localisation_App/ServicesDemoPage.html', context)

    context = {
        "service": "onscreenkeyboard",
        "data": "onscreenkeyboard",
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,

    }
    return render(request, 'Localisation_App/ServicesDemoPage.html', context)


def srvTTS(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
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
            r = requests.post(url, data=payload)
            print('response', r)
            if r.status_code == 200:
                data = r.json()
                print('response', data)
                print('file', data['outspeech_filepath'][0])
                context = {
                    'Status': data['status'],
                    'outspeech_filepath': data['outspeech_filepath'][0],
                    "service": "srvTTS",
                    "TTS_Form": tTS_Form,
                    "data": "srvTTS",
                    'topmenus': TopMenuItemsdata,
                    'FooterMenuItemsdata': FooterMenuItemsdata,
                }
                print("returned")
                return render(request, 'Localisation_App/ServicesDemoPage.html', context)

    context = {
        "service": "srvTTS",
        "TTS_Form": tTS_Form,
        "data": "srvTTS",
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        "DIVTITLE": "HELLO"
    }
    return render(request, 'Localisation_App/ServicesDemoPage.html', context)


def srvTransliteration(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    if request.method == "POST":
        context = {
            "service": "srvTransliteration",
            "data": "srvTransliteration",
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
        }
        return render(request, 'Localisation_App/ServicesDemoPage.html', context)

    context = {
        "service": "srvTransliteration",
        "data": "srvTransliteration",
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,

    }
    return render(request, 'Localisation_App/ServicesDemoPage.html', context)


# Faqs Page
def faqs(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    faqs_data = FAQs.objects.all()
    context = {
        'data': faqs_data,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'topmenus': TopMenuItemsdata,
        'faq_title': 'none'
    }
    return render(request, 'Localisation_App/faqs.html', context)


def faqsSearch(request, faq_title):
    print("titlenone", faq_title)
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    faqs_data = FAQs.objects.all()
    count = faqs_data.count()

    if request.method == "POST":
        print("insideSearchMethod")
        print(faq_title)
        faq_title1 = request.POST.get("faq_title")
        print("faqtitle", faq_title1)

        if faq_title1 != '':
            fAQs_Data = FAQs.objects.filter(
                FAQs_Question__icontains=faq_title1)
            count = fAQs_Data.count()
            print("faqcount", count)
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'data': fAQs_Data,
                'faq_title': faq_title1,
                'count': count
            }
            return render(request, 'Localisation_App/faqs.html', context)
        else:
            count = faqs_data.count()
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'data': faqs_data,
                'faq_title': 'none',
                'count': count
            }
            return render(request, 'Localisation_App/faqs.html', context)

    return render(request, 'Localisation_App/faqs.html', context)


# Terms And Conditions
def termsandcondition(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    footer_data = Footer_Links.objects.get(
        Footer_Links_Title__contains='Terms & Conditions')
    print("hello", footer_data)
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'content': footer_data

    }
    return render(request, 'Localisation_App/termsandconditions.html', context)

# accessibility statement


def accessibilityStatement(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    footer_data = Footer_Links.objects.get(
        Footer_Links_Title__contains='Accessibility Statement')
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'content': footer_data
    }
    return render(request, 'Localisation_App/accessibility_statement.html', context)

# websitepolicies


def websitepolicy(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    footer_sub_data = Footer_Links_Info.objects.all().filter(
        Footer_Links_Info_MainTitle__Footer_Links_Title__contains="Website Policies")
    content = Footer_Links_Info.objects.all().filter(
        Footer_Links_Info_SubTitle="Copyright Policy")[0]
    print(content)
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'footer_sub_data': footer_sub_data,
        "content": content
    }
    return render(request, 'Localisation_App/websitepolicies.html', context)

# websitepolicies


def websitepolicydata(request, id):
    print("id : ", id)
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    # main_footer_data = Footer_Links.objects.all()
    footer_sub_data = Footer_Links_Info.objects.all().filter(
        Footer_Links_Info_MainTitle__Footer_Links_Title__contains="Website Policies")
    content = Footer_Links_Info.objects.get(pk=id)
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'footer_sub_data': footer_sub_data,
        "content": content
    }
    return render(request, 'Localisation_App/websitepolicies.html', context)

# Sitemap Page


def sitemap(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    footer_data = Footer_Links.objects.get(
        Footer_Links_Title__contains='Sitemap')
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'content': footer_data
    }
    return render(request, 'Localisation_App/sitemap.html', context)

# Help Page


def helpData(request, id):
    print("id : ", id)
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    footer_sub_data = Footer_Links_Info.objects.all().filter(
        Footer_Links_Info_MainTitle__Footer_Links_Title__contains="help")
    print("Help ", footer_sub_data)
    content = Footer_Links_Info.objects.get(pk=id)
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        "footer_sub_data": footer_sub_data,
        "content": content
    }
    return render(request, 'Localisation_App/help.html', context)

# help


def help(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    footer_sub_data = Footer_Links_Info.objects.all().filter(
        Footer_Links_Info_MainTitle__Footer_Links_Title__contains="help")
    content = Footer_Links_Info.objects.all().filter(
        Footer_Links_Info_SubTitle="Screen Reader Access")[0]
    print(content)
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        "footer_sub_data": footer_sub_data,
        "content": content
    }
    return render(request, 'Localisation_App/help.html', context)


def contactus(request):
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    footer_sub_data = Footer_Links_Info.objects.all().filter(
        Footer_Links_Info_MainTitle__Footer_Links_Title__contains="help")
    TopMenuItemsdata = TopMenuItems.objects.all()
    num = random.randrange(1121, 9899)

    str_num = str(num)
    context = {
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'footer_sub_data': footer_sub_data,
        'topmenus': TopMenuItemsdata,
        'img': str_num
    }

    return render(request, 'Localisation_App/contactus.html', context)


def submit(request, img):
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

            res = send_mail("feedback", "Feedback Recieved",
                            "tanvip@cdac.in", [email])
            print("reponse form email", res)
            messages.add_message(request, messages.SUCCESS,
                                 'feedback submitted successfully')
            print(messages)
            return redirect('Localisation_App:contactus')
    #    return HttpResponse("form submitted successfully")
        else:
            messages.add_message(request, messages.ERROR,
                                 'feeback submission failed')
            return redirect('Localisation_App:contactus')
    else:
        messages.add_message(request, messages.ERROR, 'server error')
        return redirect('Localisation_App:contactus')


def Register_user(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    form = RegisterForm()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'form': form
    }
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print("Form Data")
            UserRegistration.objects.create(userregistration_first_name=form.cleaned_data.get('first_name'), userregistration_middle_name=form.cleaned_data.get('middle_name'), userregistration_last_name=form.cleaned_data.get('last_name'), userregistration_username=form.cleaned_data.get('username'), userregistration_email_field=form.cleaned_data.get(
                'email'), userregistration_phone_number=form.cleaned_data.get('phone_number'), userregistration_address=form.cleaned_data.get('address'), userregistration_password=form.cleaned_data.get('password1'), userregistration_confirm_password=form.cleaned_data.get('password2'), userregistration_active_status=form.cleaned_data.get('check'), registration_User_Type=form.cleaned_data.get('User_Type'))
            messages.success(request, 'Account was created for ' +
                             form.cleaned_data.get('first_name'))
            return redirect('/')
        else:
            print('Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'form': form
            }
            return render(request, 'Localisation_App/register.html', context)
    return render(request, 'Localisation_App/register.html', context)


def login_user(request):
    form = UserLoginForm()
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        print(request.POST.get('username'))
        print(request.POST.get('password'))
        if form.is_valid():
            print("loginform")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print("if form is valid")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/')

        else:
            messages.error(request, 'Error Processing Your Request')
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'form': UserLoginForm()
            }
            print("else")
            return render(request, 'Localisation_App/login.html', context)
    else:
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'form': UserLoginForm()
        }
        return render(request, 'Localisation_App/login.html', context)


def logout_user(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,

    }
    logout(request)
    return render(request, 'Localisation_App/logout.html', context)


def changePassword(request,token):
    form = UserChangePasswordForm()
    user_Profile_obj=UserRegistration.objects.get(userregistration_token = token)
    if user_Profile_obj is not None:    
        print("inside change padsword",user_Profile_obj.pk)
        if request.method == 'POST':
            form = UserChangePasswordForm(data=request.POST)
            if form.is_valid():
                print("inside Post") 
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                user_id = request.POST.get('user_id')
            
                if user_id is None:
                    messages.success(request, 'User Not Found')
                    return redirect('Localisation_App:forgetPassword')
                
                user_Register_obj=UserRegistration.objects.get(pk=user_id)
                user_Register_obj.userregistration_password = password1
                user_Register_obj.userregistration_confirm_password = password2
                user_Register_obj.save()
                
                # Main_User_Object=User.objects.get(username = user_Register_obj.userregistration_username)
                # Main_User_Object.set_password(password1)
                # Main_User_Object.save()
                # print("mainUser",Main_User_Object)
                
                
                # print("updated User",UserRegistration.objects.get(pk=user_id))
                print('Password Reset Successfully ')
                return redirect('Localisation_App:forgetPassword')
        
        user_id=user_Profile_obj.pk
        context = {
            'form': form,
            'User_Id':user_id
        }
        return render(request, 'Localisation_App/changePassword.html',context)
    else:
        messages.success(request, 'User Not Found')
        print('User Not Found')
        return redirect('Localisation_App:forgetPassword')
   
           
   
    
    


def forgetPassword(request):
    form =UserForgetPasswordForm()
    try:
        if request.method == 'POST':
            form = UserForgetPasswordForm(data=request.POST)
            if form.is_valid():
                print('insideValidmethod')
                username = form.cleaned_data['username']
                if not User.objects.filter(username = username).first():
                    messages.success(request, 'No user found with this username')
                    print('No user found with this username')
                    return redirect('Localisation_App:forgetPassword')
                user_obj=User.objects.get(username = username)
                token=str(uuid.uuid4())
                user_Profile_obj=UserRegistration.objects.get(userregistration_username = username)
                user_Profile_obj.userregistration_token = token
                user_Profile_obj.save()
                send_forget_password_email(user_Profile_obj.userregistration_email_field,token)
                print("userdata",user_obj)
                
                
                messages.success(request, 'An email is sent')
                print('An email is sent')
                context={
                    'form':form
                }
                return redirect('Localisation_App:forgetPassword',context)
         
            
    except Exception as e:
        print(e)
    context={
        'form':form
    }
    return render(request, 'Localisation_App/forgetPassword.html',context)





def goTranslate(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        "service": "goTranslate"
    }
    return render(request, 'Localisation_App/ServicesDemoPage.html', context)


def dashboard(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    SuccessStoriescategory_name = []
    countOfStoriesWithCategory = []
    successStories_CategoryData = SuccessStories_Category.objects.all()

    toolscategory_name = []
    countOfToolsWithCategory = []
    toolsCategory_data = Tools_Category.objects.all()

    resourcescategory_name = []
    countOfResourcesWithCategory = []
    resourcesCategory_data = Resources_Category.objects.all()

    userType = []
    userType_Duplicate = []
    userCount_Per_Type = []
    userRegistration_Data = UserRegistration.objects.all()

    guidelinesType = []
    guidelines_Duplicate = []
    guidelinesCount_Per_Type = []
    guidelines_data = GuidelinceForIndianGovWebsite.objects.all()

    toolsName = []
    id = []
    toolsName_hitCount_Per_Name = []
    tools_data = ToolsData.objects.all()

    resourcesName = []
    id_resources = []
    resourcesName_hitCount_Per_Name = []
    resources_data = ResourceData.objects.all()

    for n in successStories_CategoryData:
        SuccessStoriescategory_name.append(n.SuccessStories_CategoryType)
    for n in successStories_CategoryData:
        count = SuccessStories.objects.filter(
            SuccessStories_category__SuccessStories_CategoryType=n.SuccessStories_CategoryType).count()
        countOfStoriesWithCategory.append(count)

    for n in toolsCategory_data:
        toolscategory_name.append(n.Tools_CategoryType)
    for n in toolsCategory_data:
        count = ToolsData.objects.filter(
            ToolsData_CategoryType__Tools_CategoryType=n.Tools_CategoryType).count()
        countOfToolsWithCategory.append(count)

    for n in resourcesCategory_data:
        resourcescategory_name.append(n.Resources_CategoryType)
    for n in resourcesCategory_data:
        count = ResourceData.objects.filter(
            ResourceData_CategoryType__Resources_CategoryType=n.Resources_CategoryType).count()
        countOfResourcesWithCategory.append(count)

    for n in userRegistration_Data:
        userType_Duplicate.append(n.registration_User_Type)
    data_unique = set(userType_Duplicate)
    userType = list(data_unique)
    for n in userType:
        count = UserRegistration.objects.filter(
            registration_User_Type=n).count()
        userCount_Per_Type.append(count)

    for n in guidelines_data:
        guidelines_Duplicate.append(n.name)
    data_unique = set(guidelines_Duplicate)
    guidelinesType = list(data_unique)
    for n in guidelinesType:
        # print(n)
        data = GuidelinceForIndianGovWebsite.objects.values(
            'percentage').filter().get(name=n)

        guidelinesCount_Per_Type.append(data["percentage"])

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

    # # print("cat",toolsName)
    # # print("data",toolsName_hitCount_Per_Name)

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

    print("cat", resourcesName)
    print("data", resourcesName_hitCount_Per_Name)

    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'name': 'Success Strories Dataset',
        'successStories_CategoryData': SuccessStoriescategory_name,
        'count_Of_Stories_PerCategory': countOfStoriesWithCategory,

        'tools_CategoryData': toolscategory_name,
        'count_Of_Tools_PerCategory': countOfToolsWithCategory,

        'resources_CategoryData': resourcescategory_name,
        'count_Of_Resources_PerCategory': countOfResourcesWithCategory,

        'user_CategoryData': userType,
        'count_Of_User_PerCategory': userCount_Per_Type,


        'guidelinesType': guidelinesType,
        'guidelinesCount_Per_Type': guidelinesCount_Per_Type,


        'toolshit_name': toolsName,
        'toolsHitCount': toolsName_hitCount_Per_Name,

        'resourcesshit_name': resourcesName,
        'resourcesHitCount': resourcesName_hitCount_Per_Name

    }
    return render(request, 'Localisation_App/Dashboard.html', context)


# Translation Quote
def translation_quote(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()

    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
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

    #         return render(request, "Localisation_App/translation_quote.html", context)
    #     except ValidationError as e:
    #         context['error_message'] = e.message
    #         return render(request, "Localisation_App/translation_quote.html", context)

    # return render(request, "Localisation_App/translation_quote.html", context)

    """ 
    OLD CODE ENDS HERE
    
    """

    form = TranslationQuoteForm()
    context['form'] = form

    if request.method == 'POST':
        url = request.POST.get('url')
        language = request.POST.get('language')
        website_type = request.POST.get('website_type')
        delivery_date = request.POST.get('delivery_date')

        form = TranslationQuoteForm(request.POST)

        context['form'] = form
        print("dsnghufdygiu")
        if form.is_valid():
            print("validation success")
            print(form.cleaned_data['url'])
            print(form.cleaned_data['language'])
            print(form.cleaned_data['website_type'])
            print(form.cleaned_data['delivery_date'])

            data = TranslationQuote(
                url=url, language=language, website_type=website_type, delivery_date=delivery_date)
            data.save()
            context['status'] = 'success'
            context['message'] = "Form submitted successfully"

            return render(request, 'Localisation_App/translation_quote.html', context)
        else:
            context['status'] = 'error'
            context['message'] = "Invalid URL!"

            # messages.error(request, 'Error Processing Your Request')

            return render(request, 'Localisation_App/translation_quote.html', context)

    return render(request, "Localisation_App/translation_quote.html", context)


def dashboard2(request):
    SuccessStoriescategory_name = []
    countOfStoriesWithCategory = []
    successStories_CategoryData = SuccessStories_Category.objects.all()

    toolscategory_name = []
    countOfToolsWithCategory = []
    toolsCategory_data = Tools_Category.objects.all()

    resourcescategory_name = []
    countOfResourcesWithCategory = []
    resourcesCategory_data = Resources_Category.objects.all()

    userType = []
    userType_Duplicate = []
    userCount_Per_Type = []
    userRegistration_Data = UserRegistration.objects.all()

    guidelinesType = []
    guidelines_Duplicate = []
    guidelinesCount_Per_Type = []
    guidelines_data = GuidelinceForIndianGovWebsite.objects.all()

    toolsName = []
    id = []
    toolsName_hitCount_Per_Name = []
    tools_data = ToolsData.objects.all()

    for n in successStories_CategoryData:
        SuccessStoriescategory_name.append(n.SuccessStories_CategoryType)
    for n in successStories_CategoryData:
        count = SuccessStories.objects.filter(
            SuccessStories_category__SuccessStories_CategoryType=n.SuccessStories_CategoryType).count()
        countOfStoriesWithCategory.append(count)

    for n in toolsCategory_data:
        toolscategory_name.append(n.Tools_CategoryType)
    for n in toolsCategory_data:
        count = ToolsData.objects.filter(
            ToolsData_CategoryType__Tools_CategoryType=n.Tools_CategoryType).count()
        countOfToolsWithCategory.append(count)

    for n in resourcesCategory_data:
        resourcescategory_name.append(n.Resources_CategoryType)
    for n in resourcesCategory_data:
        count = ResourceData.objects.filter(
            ResourceData_CategoryType__Resources_CategoryType=n.Resources_CategoryType).count()
        countOfResourcesWithCategory.append(count)

    for n in userRegistration_Data:
        userType_Duplicate.append(n.registration_User_Type)
    data_unique = set(userType_Duplicate)
    userType = list(data_unique)
    for n in userType:
        count = UserRegistration.objects.filter(
            registration_User_Type=n).count()
        userCount_Per_Type.append(count)

    for n in guidelines_data:
        guidelines_Duplicate.append(n.name)
    data_unique = set(guidelines_Duplicate)
    guidelinesType = list(data_unique)
    for n in guidelinesType:
        # print(n)
        data = GuidelinceForIndianGovWebsite.objects.values(
            'percentage').filter().get(name=n)
        print(data["percentage"])
        guidelinesCount_Per_Type.append(data["percentage"])

    for n in tools_data:
        id.append(n.id)
    print(id)
    for n in id:
        # print(n)
        data = ToolsData.objects.values('ToolsData_DownloadCounter').get(id=n)
        # print(data)
        print(data["ToolsData_DownloadCounter"])
        toolsName_hitCount_Per_Name.append(data["ToolsData_DownloadCounter"])

    for n in id:
        datname = ToolsData.objects.values('ToolsData_HeadingName').get(id=n)
        toolsName.append(datname["ToolsData_HeadingName"])
        print(datname["ToolsData_HeadingName"])

    # # print("cat",toolsName)
    # # print("data",toolsName_hitCount_Per_Name)

    context = {
        'name': 'Success Strories Dataset',
        'successStories_CategoryData': SuccessStoriescategory_name,
        'count_Of_Stories_PerCategory': countOfStoriesWithCategory,

        'tools_CategoryData': toolscategory_name,
        'count_Of_Tools_PerCategory': countOfToolsWithCategory,

        'resources_CategoryData': resourcescategory_name,
        'count_Of_Resources_PerCategory': countOfResourcesWithCategory,

        'user_CategoryData': userType,
        'count_Of_User_PerCategory': userCount_Per_Type,


        'guidelinesType': guidelinesType,
        'guidelinesCount_Per_Type': guidelinesCount_Per_Type,


        'toolshit_name': toolsName,
        'toolsHitCount': toolsName_hitCount_Per_Name,



    }
    return render(request, 'Localisation_App/dashboard2.html', context)


def machine_translation(request):
    return render(request,'Localisation_App/machine_translation.html')

def name_matcher(request):
    return render(request,'Localisation_App/name_matcher.html')
