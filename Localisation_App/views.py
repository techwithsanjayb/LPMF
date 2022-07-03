from .forms import ServiceForm, TTSservice
from django.core.mail import send_mail, mail_admins
# import requests
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from html.parser import HTMLParser
from multiprocessing import context
from django.shortcuts import render, redirect
from pip import main
from .models import Article, SuccessStories, ResourceData, FAQs, NewsAndEvents, Services, ToolsData, TopMenuItems, SuccessStrories_Category, Footer_Links, Footer_Links_Info, ToolsData, Tools_Category, FooterMenuItems, Tools_Searched_Title, Resources_Category, Contact
from django.views.generic.list import ListView
from html.parser import HTMLParser
import random
global str_num

#from .models import Article
# Create your views here.

# def home(request):

#     x=request.path_info
#     print(x)
#     y=x.replace("/", "")
#     content = Article.objects.get(Article_Menu_ID=4)
#     print("content is ")
#     print(content)
#     if request.method =="GET":
#         print(request.method)

#     return render(request, 'Localisation_App/home2.html' ,{'data': content})


# def index(request):
#     return render(request, 'Localisation_App/test.html')


# class SuccessStoriesList(ListView):
#     model = SuccessStories
#     context_object_name = 'SuccessStoriesList'
#     template_name= "xxxxxxxx.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['SuccessStoriesList']=context['SuccessStoriesList'].filter(User=self.request.user)
#         # context['tasks']=context['tasks'].filter(user=self.request.user)
#
#         return context

Tools_Searched_Value = ""


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
    ArticleData = Article.objects.all()
    SuccessStoriesData = SuccessStories.objects.all()
    Servicesdata = Services.objects.all()
    NewsAndEventsData = NewsAndEvents.objects.all()

    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'ArticleData': ArticleData,
        'SuccessStoriesData': SuccessStoriesData,
        'NewsAndEventsData': NewsAndEventsData,
        'Servicesdata': Servicesdata
    }
    return render(request, 'Localisation_App/home.html', context)


# About Us Page

def aboutus(request):
    print("hello")
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    ArticleData = Article.objects.all().filter(Article_HeadingName="About Us")
    print("TEst ", ArticleData)
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'ArticleData': ArticleData,
    }
    return render(request, 'Localisation_App/aboutus.html', context)

# Tools Page


def toolsPage(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    ToolsCategory_data = Tools_Category.objects.all()
    Tools_Data = ToolsData.objects.all()
    Tools_Category.objects.all().update(Tools_Cat_Status=False)
    count = ToolsData.objects.all().count()
    page = Paginator(Tools_Data, 7)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    count = Tools_Data.count()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'toolsdata': Tools_Data,
        'tools_title': 'none',
        'toolscategory': ToolsCategory_data,
        "page": page,
        'satus_All_Checked': 'True',
        'Pagination_Type': 'All_Data',
        'count': count
    }
    return render(request, 'Localisation_App/tools.html', context)


def tools(request):
    checklist1 = []
    category_name = []
    pagestatus = False
    q = ToolsData.objects.none()
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    ToolsCategory_data = Tools_Category.objects.all()
    Tools_Data = ToolsData.objects.all()
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
            ToolsData_Checked = Tools_Category.objects.filter(id__in=checklist)
            for n in ToolsData_Checked:
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
            page = Paginator(q, 7)
            page_list = request.GET.get('page')
            # print("pagenumber",page_list)
            page = page.get_page(page_list)

            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'toolsdata': q,
                'tools_title': 'none',
                'toolscategory': ToolsCategory_data,
                "page": page,
                'satus_All_Checked': None,
                'Pagination_Type': 'Category_Post',
                'count': count
            }
            print("inside 1")
            # return render(request,'Localisation_App/tools.html',context)
            return render(request, 'Localisation_App/tools.html', context)
        else:
            page = Paginator(Tools_Data, 7)
            Tools_Category.objects.all().update(Tools_Cat_Status=False)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = ToolsData.objects.all().count()
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'toolsdata': Tools_Data,
                'tools_title': 'none',
                'toolscategory': ToolsCategory_data,
                "page": page,
                'satus_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
            print("inside 2")
            return render(request, 'Localisation_App/tools.html', context)
    for p in ToolsCategory_data:
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
        page = Paginator(q, 7)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = q.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'toolsdata': q,
            'tools_title': 'none',
            'toolscategory': ToolsCategory_data,
            "page": page,
            'satus_All_Checked': None,
            'Pagination_Type': 'Category_Post',
            'count': count
        }

    else:
        page = Paginator(Tools_Data, 7)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = Tools_Data.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'toolsdata': Tools_Data,
            'tools_title': 'none',
            'toolscategory': ToolsCategory_data,
            "page": page,
            'satus_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count
        }
    # print("toolssaerchedvalue",Tools_Searched_Value)
    return render(request, 'Localisation_App/tools.html', context)


def toolsSearch(request, tools_title):
    print("titlenone", tools_title)
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    ToolsCategory_data = Tools_Category.objects.all()
    Tools_Data = ToolsData.objects.all()

    if request.method == "POST":
        print("insideSearchMethod")
        print(tools_title)
        tools_title1 = request.POST.get("toolname")
        print("toolstitile", tools_title1)

        if tools_title1 != '':
            Tools_Data = ToolsData.objects.filter(
                ToolsData_HeadingName__icontains=tools_title1)
            count = Tools_Data.count()
            print("datatooldssds", count)
            page = Paginator(Tools_Data, 7)
            page_list = request.GET.get('page')
            # print("pagenumber",page_list)
            page = page.get_page(page_list)
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'toolsdata': Tools_Data,
                'tools_title': tools_title1,
                'toolscategory': ToolsCategory_data,
                "page": page,
                'satus_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        else:
            page = Paginator(Tools_Data, 7)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = Tools_Data.count()
            print("None Selected")
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'toolsdata': Tools_Data,
                'tools_title': 'none',
                'toolscategory': ToolsCategory_data,
                "page": page,
                'satus_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        return render(request, 'Localisation_App/tools.html', context)
    if tools_title != 'none':
        Tools_Data1 = ToolsData.objects.filter(
            ToolsData_HeadingName__icontains=tools_title)
        page = Paginator(Tools_Data1, 7)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = Tools_Data1.count()
        print("hereee", Tools_Data1)
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'toolsdata': Tools_Data1,
            'tools_title': tools_title,
            'toolscategory': ToolsCategory_data,
            "page": page,
            'satus_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    else:
        page = Paginator(Tools_Data, 7)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = Tools_Data.count()
        print("None Selected")
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'toolsdata': Tools_Data,
            'tools_title': 'none',
            'toolscategory': ToolsCategory_data,
            "page": page,
            'satus_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }

    return render(request, 'Localisation_App/tools.html', context)


# Resources Page
def resourcesPage(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    ResoucesCategory_data = Resources_Category.objects.all()
    Resources_Data = ResourceData.objects.all()
    Resources_Category.objects.all().update(Resources_Cat_Status=False)
    count = ResourceData.objects.all().count()
    page = Paginator(Resources_Data, 7)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    count = Resources_Data.count()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'resoucesdata': Resources_Data,
        'resource_title': 'none',
        'resourcescategory': ResoucesCategory_data,
        "page": page,
        'satus_All_Checked': 'True',
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
    ResoucesCategory_data = Resources_Category.objects.all()
    Resources_Data = ResourceData.objects.all()
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
            ResourcesData_Checked = Resources_Category.objects.filter(
                id__in=checklist)
            for n in ResourcesData_Checked:
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
            page = Paginator(q, 7)
            page_list = request.GET.get('page')
            # print("pagenumber",page_list)
            page = page.get_page(page_list)

            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'resoucesdata': q,
                'resource_title': 'none',
                'resourcescategory': ResoucesCategory_data,
                "page": page,
                'satus_All_Checked': None,
                'Pagination_Type': 'Category_Post',
                'count': count
            }
            print("inside 1")

            return render(request, 'Localisation_App/resources.html', context)
        else:
            page = Paginator(Resources_Data, 7)
            Resources_Category.objects.all().update(Resources_Cat_Status=False)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = Resources_Data.count()
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'resoucesdata': Resources_Data,
                'resource_title': 'none',
                'resourcescategory': ResoucesCategory_data,
                "page": page,
                'satus_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
            print("inside 2")
            return render(request, 'Localisation_App/resources.html', context)
    for p in ResoucesCategory_data:
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
        page = Paginator(q, 7)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = q.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'resoucesdata': q,
            'resource_title': 'none',
            'resourcescategory': ResoucesCategory_data,
            "page": page,
            'satus_All_Checked': None,
            'Pagination_Type': 'Category_Post',
            'count': count
        }

    else:
        page = Paginator(Resources_Data, 7)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = Resources_Data.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'resoucesdata': Resources_Data,
            'resource_title': 'none',
            'resourcescategory': ResoucesCategory_data,
            "page": page,
            'satus_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count
        }

    return render(request, 'Localisation_App/resources.html', context)


def resourceSearch(request, resource_title):
    print("titlenone", resource_title)
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    ResoucesCategory_data = Resources_Category.objects.all()
    Resources_Data = ResourceData.objects.all()
    count = ResourceData.objects.all().count()

    if request.method == "POST":
        print("insideSearchMethod")
        print(resource_title)
        resource_title1 = request.POST.get("resourcename")
        print("resourcestitle", resource_title1)

        if resource_title1 != '':
            Resource_Data = ResourceData.objects.filter(
                ResourceData_HeadingName__icontains=resource_title1)
            count = Resource_Data.count()
            print("dataresourcesdssds", count)
            page = Paginator(Resource_Data, 7)
            page_list = request.GET.get('page')
            # print("pagenumber",page_list)
            page = page.get_page(page_list)
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'resoucesdata': Resource_Data,
                'resource_title': resource_title1,
                'resourcescategory': ResoucesCategory_data,
                "page": page,
                'satus_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        else:
            page = Paginator(Resources_Data, 7)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = Resources_Data.count()
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'resoucesdata': Resources_Data,
                'resource_title': 'none',
                'resourcescategory': ResoucesCategory_data,
                "page": page,
                'satus_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        return render(request, 'Localisation_App/resources.html', context)
    if resource_title != 'none':
        Resource_Data1 = ResourceData.objects.filter(
            ResourceData_HeadingName__icontains=resource_title)
        page = Paginator(Resource_Data1, 7)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = Resource_Data1.count()
        print("hereee", Resource_Data1)
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'resoucesdata': Resource_Data1,
            'resource_title': resource_title,
            'resourcescategory': ResoucesCategory_data,
            "page": page,
            'satus_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    else:
        page = Paginator(Resources_Data, 7)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = Resources_Data.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'resoucesdata': Resources_Data,
            'resource_title': 'none',
            'resourcescategory': ResoucesCategory_data,
            "page": page,
            'satus_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }

    return render(request, 'Localisation_App/resources.html', context)

# Successstory Page


def successstoryPage(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    SuccessStrories_Category.objects.update(SuccessStrories_Cat_Status=False)
    SuccessStrories_CategoryData = SuccessStrories_Category.objects.all()
    SuccessStoriesData = SuccessStories.objects.all()
    page = Paginator(SuccessStoriesData, 7)
    # SuccessStrories_Category.objects.all().update(SuccessStrories_Cat_Status=False)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    count = SuccessStoriesData.count()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'SuccessStoriesData': SuccessStoriesData,
        'SuccessStrories_CategoryData': SuccessStrories_CategoryData,
        'story_title': 'none',
        "page": page,
        'satus_All_Checked': 'True',
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
    SuccessStrories_CategoryData = SuccessStrories_Category.objects.all()
    SuccessStoriesData = SuccessStories.objects.all()

    if request.method == "POST":
        # print("allcheched",request.POST.get('all_checkbox'))
        if request.POST.get('all_checkbox') != 'all_Checked':
            category_name = []
            q = SuccessStories.objects.none()
            # print("dumydata",q)
            checklist = request.POST.getlist('checkbox')
            # print(checklist)
            SuccessStrories_Category.objects.all().update(SuccessStrories_Cat_Status=False)
            for n in checklist:
                SuccessStrories_Category.objects.filter(
                    pk=int(n)).update(SuccessStrories_Cat_Status=True)
            SuccessStoriesData_Checked = SuccessStrories_Category.objects.filter(
                id__in=checklist)
            for n in SuccessStoriesData_Checked:
                # print('hello',n.SuccessStrories_CategoryType)
                category_name.append(n.SuccessStrories_CategoryType)
            # print("list",category_name)
            # print("tuple",tuple(category_name))
            to_fetch = tuple(category_name)

            for c in to_fetch:
                # print(c)
                q = q | SuccessStories.objects.filter(
                    SuccessStories_category__SuccessStrories_CategoryType__contains=c)
            # print("all data",q)
            count = q.count()
            print("hey", q)
            page = Paginator(q, 7)
            page_list = request.GET.get('page')
            # print("pagenumber",page_list)
            page = page.get_page(page_list)
            count = q.count()

            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'SuccessStoriesData': q,
                'SuccessStrories_CategoryData': SuccessStrories_CategoryData,
                "page": page,
                'story_title': 'none',
                'Pagination_Type': 'Category_Post',
                'satus_All_Checked': None,
                'count': count
            }
            print("inside 1")
            # return render(request,'Localisation_App/successstory.html',context)

        else:
            page = Paginator(SuccessStoriesData, 7)
            SuccessStrories_Category.objects.all().update(SuccessStrories_Cat_Status=False)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = SuccessStoriesData.count()
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'SuccessStoriesData': SuccessStoriesData,
                'SuccessStrories_CategoryData': SuccessStrories_CategoryData,
                "page": page,
                'story_title': 'none',
                'satus_All_Checked': 'True',
                'Pagination_Type': 'All_Data',
                'count': count
            }
            print("inside 2")

    for p in SuccessStrories_CategoryData:
        if p.SuccessStrories_Cat_Status == True:
            print("true")
            pagestatus = True
            category_name.append(p.SuccessStrories_CategoryType)
    to_fetch = tuple(category_name)
    for c in to_fetch:
        q = q | SuccessStories.objects.filter(
            SuccessStories_category__SuccessStrories_CategoryType__contains=c)
    print(q)

    if pagestatus == True:
        page = Paginator(q, 7)
        # SuccessStrories_Category.objects.all().update(SuccessStrories_Cat_Status=False)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = q.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'SuccessStoriesData': q,
            'story_title': 'none',
            'SuccessStrories_CategoryData': SuccessStrories_CategoryData,
            "page": page,
            'Pagination_Type': 'Category_Post',
            'satus_All_Checked': None,
            'count': count
        }

    else:
        page = Paginator(SuccessStoriesData, 7)
        # SuccessStrories_Category.objects.all().update(SuccessStrories_Cat_Status=False)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = SuccessStoriesData.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'SuccessStoriesData': SuccessStoriesData,
            'story_title': 'none',
            'SuccessStrories_CategoryData': SuccessStrories_CategoryData,
            "page": page,
            'satus_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count
        }

    print("outside")
    return render(request, 'Localisation_App/successstory.html', context)


def successstorySearch(request, story_title):
    print("titlenone", story_title)
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    SuccessStrories_CategoryData = SuccessStrories_Category.objects.all()
    SuccessStoriesData = SuccessStories.objects.all()

    if request.method == "POST":
        print("insideSearchMethod")
        print(story_title)
        strory_title1 = request.POST.get("storyname")
        print("strory_title1", strory_title1)

        if strory_title1 != '':
            SuccessStoriesData = SuccessStories.objects.filter(
                SuccessStories_TitleName__icontains=strory_title1)
            count = SuccessStoriesData.count()
            print("dataStoriesdssds", count)
            page = Paginator(SuccessStoriesData, 7)
            page_list = request.GET.get('page')
            # print("pagenumber",page_list)
            page = page.get_page(page_list)
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'story_title': strory_title1,
                'SuccessStoriesData': SuccessStoriesData,
                'SuccessStrories_CategoryData': SuccessStrories_CategoryData,
                "page": page,
                'satus_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        else:
            page = Paginator(SuccessStoriesData, 7)
            page_list = request.GET.get('page')
            page = page.get_page(page_list)
            count = SuccessStoriesData.count()
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'SuccessStoriesData': SuccessStoriesData,
                'story_title': 'none',
                'SuccessStrories_CategoryData': SuccessStrories_CategoryData,
                "page": page,
                'satus_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        return render(request, 'Localisation_App/successstory.html', context)
    if story_title != 'none':
        Stories_Data1 = SuccessStories.objects.filter(
            SuccessStories_TitleName__icontains=story_title)
        page = Paginator(Stories_Data1, 7)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = Stories_Data1.count()
        print("hereee", Stories_Data1)
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'SuccessStoriesData': Stories_Data1,
            'story_title': story_title,
            'SuccessStrories_CategoryData': SuccessStrories_CategoryData,
            "page": page,
            'satus_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    else:
        page = Paginator(SuccessStoriesData, 7)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = SuccessStoriesData.count()
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'SuccessStoriesData': SuccessStoriesData,
            'story_title': 'none',
            'SuccessStrories_CategoryData': SuccessStrories_CategoryData,
            "page": page,
            'satus_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }

    return render(request, 'Localisation_App/successstory.html', context)


# def successstory(request):
#     checklist1=[]
#     TopMenuItemsdata=TopMenuItems.objects.all()
#     SuccessStrories_CategoryData=SuccessStrories_Category.objects.all()
#     SuccessStoriesData=SuccessStories.objects.all()
#     print("helloooooo",type(SuccessStoriesData))
#     page=Paginator(SuccessStoriesData, 7)
#     page_list=request.GET.get('page')
#     page=page.get_page(page_list)
#     if request.method=="POST":
#         category_name=[]
#         q=SuccessStories.objects.filter(id=10000000)
#         print("dumydata",q)
#         checklist=request.POST.getlist('checkbox')
#         print(checklist)
#         SuccessStoriesData_Checked=SuccessStrories_Category.objects.filter(id__in=checklist)
#         for n in SuccessStoriesData_Checked:
#             print('hello',n.SuccessStrories_CategoryType)
#             category_name.append(n.SuccessStrories_CategoryType)
#         print("list",category_name)
#         print("tuple",tuple(category_name))
#         to_fetch=tuple(category_name)
#         for c in to_fetch:
#             print(c)
#             q = q | SuccessStories.objects.filter(SuccessStories_category__SuccessStrories_CategoryType__contains=c)
#         print("all data",q)
#         page=Paginator(q, 7)
#         page_list=request.GET.get('page')
#         print("pagenumber",page_list)
#         page=page.get_page(page_list)
#         context={
#             'topmenus':TopMenuItemsdata,
#             'SuccessStoriesData':q,
#             'SuccessStrories_CategoryData':SuccessStrories_CategoryData,
#             "page":page,
#             "fetcheddata":'fetcheddata',
#             'satus':'True',
#             'checklist':checklist
#         }
#         return render(request,'Localisation_App/successstory.html',context)
#     context={
#             'topmenus':TopMenuItemsdata,
#             'SuccessStoriesData':SuccessStoriesData,
#             'SuccessStrories_CategoryData':SuccessStrories_CategoryData,
#             "page":page,
#             "fetcheddata":'notfetcheddata',
#             'satus':None,
#             'checklist':checklist1
#         }

#     return render(request,'Localisation_App/successstory.html',context)


# Services Page

def services(request):
    TTS_Form = TTSservice()
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    Servicesdata = Services.objects.all()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'Servicesdata': Servicesdata,
        'TTS_Form': TTS_Form,
    }
    return render(request, 'Localisation_App/services.html', context)


def ServicesDemoPage(request):
    TTS_Form = TTSservice()
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        "service": "srvTTS",
        'TTS_Form': TTS_Form
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
    TTS_Form = TTSservice()
    if request.method == "POST":
        Details = TTSservice(request.POST)
        print("InsidePostMethod")
        if Details.is_valid():
            print('form is valid')
            Language = request.POST.get("Select_Language_Pair")
            Gender = request.POST.get("Gender")
            InputText = request.POST.get("InputText")
            print("Language", Language)
            print("Gender", Gender)
            print("InputText", InputText)

            url = 'http://localhost:8000/tts'
            payload = {'text': InputText, 'gender': Gender, 'lang': Language}
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
                    "TTS_Form": TTS_Form,
                    "data": "srvTTS",
                    'topmenus': TopMenuItemsdata,
                    'FooterMenuItemsdata': FooterMenuItemsdata,
                }
                print("returned")
                return render(request, 'Localisation_App/ServicesDemoPage.html', context)

    context = {
        "service": "srvTTS",
        "TTS_Form": TTS_Form,
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
            FAQs_Data = FAQs.objects.filter(
                FAQs_Question__icontains=faq_title1)
            count = FAQs_Data.count()
            print("faqcount", count)
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'data': FAQs_Data,
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


# SuccessStrories

def SuccessStoriesList(request):
    # SuccessStoriesdata = SuccessStories.objects.all()
    # page=Paginator(SuccessStoriesdata, 7)
    # page_list=request.GET.get('page')
    # page=page.get_page(page_list)
    # context={
    #         "page":page,
    #         "SuccessStoriesdata":SuccessStoriesdata
    #         }

    return render(request, 'xxxxx.html', context)


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


# Tools

# def ToolsDataList(request):
#     ToolsData1 = ToolsData.objects.all().filter(ToolsData_HeadingName="C-DAC GIST Data Converter")
#     data={
#         "ToolsData":ToolsData1
#     }
#     return render(request,'Localisation_App/test1.html',data)

# def ToolsDataList(request):
#     ToolsData1 = ToolsData.objects.all()
#     page=Paginator(ToolsData1, 7)
#     page_list=request.GET.get('page')
#     page=page.get_page(page_list)
#     context={
#             "page":page,
#              "ToolsData":ToolsData1
#             }
#     return render(request,'Localisation_App/test1.html',context)


# Resources
# def ResourcessDataList(request):
#     ResourceData1 = ResourceData.objects.all()
#     print("Resourcedata",ResourceData1)
#     page=Paginator(ResourceData1, 7)
#     page_list=request.GET.get('page')
#     page=page.get_page(page_list)
#     context={
#             "page":page,
#             "ResourceData":ResourceData1
#             }
#     return render(request,'Localisation_App/resourceData.html',context)


# test

# def index(request):
#     return render(request, 'Localisation_App/index.html')

# def TestRequest(request):
#     Data = Article.objects.all();
#     context={
#         "Data": Data
#     }
#     return render(request, 'Localisation_App/home.html',context)


def Keyboard(request):
    return render(request, 'Localisation_App/keyboard.html')


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
        if comment[0] != " ":
            print("condition for comment not starting with space",
                  comment[0] != " ")
            if img == captcha:
                print(name, email, contactNumber, option, comment)
                ins = Contact(name=name, email=email,
                              phone=contactNumber, option=option, comment=comment)
                ins.save()
                res = send_mail(option, option+" Recieved",
                                "tanvip@cdac.in", [email, 'sshivam@cdac.in'])
                print("reponse form email", res)
                messages.add_message(
                    request, messages.SUCCESS, option+' submitted successfully')
                print(messages)
                return redirect('Localisation_App:contactus')
                #  return HttpResponse("form submitted successfully")
            else:
                messages.add_message(
                    request, messages.ERROR, 'Captcha not matching')
                return redirect('Localisation_App:contactus')
        else:
            messages.add_message(request, messages.ERROR,
                                 'comment must not start with space')
            return redirect('Localisation_App:contactus')
    else:
        messages.add_message(request, messages.ERROR, 'server error')
        return redirect('Localisation_App:contactus')
