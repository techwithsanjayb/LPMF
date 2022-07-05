
from .forms import TTSservice,RegisterForm
from django.contrib import messages
from django.core.mail import send_mail, mail_admins
from django.core.paginator import Paginator
from multiprocessing import context
from django.shortcuts import render, redirect
from .models import Article, SuccessStories, ResourceData, FAQs, NewsAndEvents, Services, ToolsData, TopMenuItems, SuccessStories_Category, Footer_Links, Footer_Links_Info, ToolsData, Tools_Category, FooterMenuItems, Tools_Searched_Title, Resources_Category, Contact,UserRegistration
import random
import requests
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
    page = Paginator(tools_Data, 7)
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
            page = Paginator(q, 7)
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
                'satus_All_Checked': None,
                'Pagination_Type': 'Category_Post',
                'count': count
            }
            print("inside 1")
            # return render(request,'Localisation_App/tools.html',context)
            return render(request, 'Localisation_App/tools.html', context)
        else:
            page = Paginator(tools_Data, 7)
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
                'satus_All_Checked': 'True',
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
        page = Paginator(q, 7)
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
            'satus_All_Checked': None,
            'Pagination_Type': 'Category_Post',
            'count': count
        }

    else:
        page = Paginator(tools_Data, 7)
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
            page = Paginator(tools_Data, 7)
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
                'satus_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        else:
            page = Paginator(tools_Data, 7)
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
                'satus_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        return render(request, 'Localisation_App/tools.html', context)
    if tools_title != 'none':
        tools_Data1 = ToolsData.objects.filter(
            ToolsData_HeadingName__icontains=tools_title)
        page = Paginator(tools_Data1, 7)
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
            'satus_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    else:
        page = Paginator(tools_Data, 7)
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
            'satus_All_Checked': 'True',
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
    page = Paginator(tools_Data, 7)
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
        'satus_All_Checked': 'True',
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
    page = Paginator(resources_Data, 7)
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
            page = Paginator(q, 7)
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
                'satus_All_Checked': None,
                'Pagination_Type': 'Category_Post',
                'count': count
            }
            print("inside 1")

            return render(request, 'Localisation_App/resources.html', context)
        else:
            page = Paginator(resources_Data, 7)
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
                'satus_All_Checked': 'True',
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
        page = Paginator(q, 7)
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
            'satus_All_Checked': None,
            'Pagination_Type': 'Category_Post',
            'count': count
        }

    else:
        page = Paginator(resources_Data, 7)
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
            'satus_All_Checked': 'True',
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
            page = Paginator(resource_Data, 7)
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
                'satus_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        else:
            page = Paginator(resources_Data, 7)
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
                'satus_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        return render(request, 'Localisation_App/resources.html', context)
    if resource_title != 'none':
        resource_Data1 = ResourceData.objects.filter(
            ResourceData_HeadingName__icontains=resource_title)
        page = Paginator(resource_Data1, 7)
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
            'satus_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    else:
        page = Paginator(resources_Data, 7)
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
            'satus_All_Checked': 'True',
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
    page = Paginator(resources_Data, 7)
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
            'satus_All_Checked': 'True',
            'Pagination_Type': 'All_Data',
            'count': count
        }
        return render(request, 'Localisation_App/resources.html', context)
    





# Successstory Page
def successstoryPage(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    SuccessStories_Category.objects.update(SuccessStories_Cat_Status=False)
    successStories_CategoryData = SuccessStories_Category.objects.all()
    successStoriesData = SuccessStories.objects.all()
    page = Paginator(successStoriesData, 7)
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
    successStories_CategoryData = SuccessStories_Category.objects.all()
    successStoriesData = SuccessStories.objects.all()

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
                    SuccessStories_category__SuccessStories_CategoryType__contains=c)
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
                'SuccessStories_CategoryData': successStories_CategoryData,
                "page": page,
                'story_title': 'none',
                'Pagination_Type': 'Category_Post',
                'satus_All_Checked': None,
                'count': count
            }
            print("inside 1")
            # return render(request,'Localisation_App/successstory.html',context)

        else:
            page = Paginator(successStoriesData, 7)
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
                'satus_All_Checked': 'True',
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
            SuccessStories_category__SuccessStories_CategoryType__contains=c)
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
            'SuccessStories_CategoryData': successStories_CategoryData,
            "page": page,
            'Pagination_Type': 'Category_Post',
            'satus_All_Checked': None,
            'count': count
        }

    else:
        page = Paginator(successStoriesData, 7)
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
    successStories_CategoryData = SuccessStories_Category.objects.all()
    successStoriesData = SuccessStories.objects.all()

    if request.method == "POST":
        print("insideSearchMethod")
        print(story_title)
        strory_title1 = request.POST.get("storyname")
        print("strory_title1", strory_title1)

        if strory_title1 != '':
            successStoriesData = SuccessStories.objects.filter(
                SuccessStories_TitleName__icontains=strory_title1)
            count = successStoriesData.count()
            print("dataStoriesdssds", count)
            page = Paginator(successStoriesData, 7)
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
                'satus_All_Checked': 'True',
                'Pagination_Type': 'Searched_Post',
                'count': count
            }
        else:
            page = Paginator(successStoriesData, 7)
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
            'SuccessStories_CategoryData': successStories_CategoryData,
            "page": page,
            'satus_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }
    else:
        page = Paginator(successStoriesData, 7)
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
            'satus_All_Checked': 'True',
            'Pagination_Type': 'Searched_Post',
            'count': count
        }

    return render(request, 'Localisation_App/successstory.html', context)


def successstoryReset(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    SuccessStories_Category.objects.update(SuccessStories_Cat_Status=False)
    successStories_CategoryData = SuccessStories_Category.objects.all()
    successStoriesData = SuccessStories.objects.all()
    page = Paginator(successStoriesData, 7)
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
            'satus_All_Checked': 'True',
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
    form  = RegisterForm()
    context = {'form': form}
    if request.method == 'POST':
        form  = RegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            print("Form Data")
            # UserRegistration.objects.create(userregistration_first_name = form.cleaned_data.get('first_name') ,userregistration_middle_name = form.cleaned_data.get('middle_name') ,userregistration_last_name = form.cleaned_data.get('last_name'),userregistration_username = form.cleaned_data.get('username') ,userregistration_email_field = form.cleaned_data.get('email'),userregistration_phone_number = form.cleaned_data.get('phone_number') ,userregistration_address = form.cleaned_data.get('address'),userregistration_password = form.cleaned_data.get('password1'),userregistration_confirm_password = form.cleaned_data.get('password2'),userregistration_active_status = form.cleaned_data.get('check'),registration_User_Type = form.cleaned_data.get('User_Type'))
            messages.success(request, 'Account was created for ' + form.cleaned_data.get('first_name'))
            # return redirect('Localisation_App:home')
        else:
            print('Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form}
            return render(request, 'Localisation_App/register.html', context) 
    return render(request, 'Localisation_App/register.html', context)
    
    
def login_user(request):
    return render(request, 'Localisation_App/register.html', context)
    
def goTranslate(request):
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        "service": "goTranslate"
    }
    return render(request, 'Localisation_App/ServicesDemoPage.html', context)
