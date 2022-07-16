
import re
from threading import currentThread
from django.db.models import Sum
from .forms import TTSservice, RegisterForm, TranslationQuoteForm, UserLoginForm, UserChangePasswordForm, UserForgetPasswordForm
from django.contrib import messages
from django.core.mail import send_mail, mail_admins
from django.core.paginator import Paginator
from multiprocessing import context
from django.contrib.auth import login, authenticate, logout,  update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.shortcuts import render, redirect
from .models import Article, EmpanelledAgencies, EmpanelledAgenciesEmail, SuccessStories, ResourceData, FAQs, NewsAndEvents, Services, ToolsData, TopMenuItems, SuccessStories_Category, Footer_Links, Footer_Links_Info, ToolsData, Tools_Category, FooterMenuItems, Tools_Searched_Title, Resources_Category, Contact, TranslationQuote, UserRegistration, GuidelinceForIndianGovWebsite
import random
import requests
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
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
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging
from datetime import date
logger = logging.getLogger('django')
global str_num

# Menu
global url


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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    tools_Data = ToolsData.objects.all()
    # print("toolsdata",tools_Data['get_ResourcesData_slug_splited'])
    # for d in tools_Data:
    #     print("data",d['get_ToolsData_slug_splited'])

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
    if request.user.is_authenticated:
        return render(request, 'Localisation_App/tools.html', context)
    else:
        return render(request, 'Localisation_App/tools.html', context)


def tools(request):
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
    tools_searchData = tools_title.replace(" ", "-")
    print("titlenone", tools_title)
    print("replace space ", tools_title.replace(" ", "-"))

    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    toolsCategory_data = Tools_Category.objects.all()
    tools_Data = ToolsData.objects.all()

    if request.method == "POST":
        print("insideSearchMethod")
        print(tools_title)

        tools_title12 = request.POST.get("toolname")
        print("resourcestitle", tools_title12)
        tools_searchData1 = tools_title12.replace(" ", "-")

        if tools_searchData1 != '':
            tools_Data = ToolsData.objects.filter(
                ToolsData_slug__icontains=tools_searchData1)
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
                'tools_title': tools_searchData1,
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
    if tools_searchData != 'none':
        tools_Data1 = ToolsData.objects.filter(
            ToolsData_slug__icontains=tools_searchData)
        page = Paginator(tools_Data1, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = tools_Data1.count()
        print("hereee", tools_Data1)
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'toolsdata': tools_Data1,
            'tools_title': tools_searchData,
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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


def toolsDownloadCounter(request, id):
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
    savedTimeInSession = None
    time_diff = 0
    if time_posted is not None:
        print("time_posted not none")
        print(time_posted)
        print("datatatataa", type(datetime.fromisoformat(time_posted[:-1])))
        savedTimeInSession = datetime.fromisoformat(time_posted[:-1])
        dataCurrentTime = datetime.now()
        print("time", type(dataCurrentTime))
        timediff = dataCurrentTime - savedTimeInSession
        time_diff = timediff.total_seconds()
        print("timediff", timediff.total_seconds())
    else:
        print("time_posted none")
    print("saved_ip", saved_ip)

    if time_diff < 20:
        saved_ip = request.session.get('toolsDownloadCounter_ip')
    else:
        request.session['toolsDownloadCounter_ip'] = None

    if ip != saved_ip:
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
        print("after", tool_obj.ToolsData_DownloadCounter)
        return redirect('Localisation_App:toolsPage')
    else:
        print("ip is same inside second none")
        request.session['toolsDownloadCounter_ip'] = ip
        print("same and none ip first")
        data = datetime.now()
        print("time", type(data))
        data1 = json.dumps(data, default=json_util.default)
        aList = json.loads(data1)
        print("data343434", aList)
        testdata = aList['$date']
        request.session['tools_Download_time'] = testdata
        print("inside second none")
        return redirect('Localisation_App:toolsPage')


# def toolsDownloadCounter(request,id):
#     print("session time",)
#     print("requestid",id)
#     print("inside herehelloooooo")
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     ip=''
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[-1].strip()
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     print("ip",ip)
#     # request.session['tools_Download_time'] = None
#     # request.session['toolsDownloadCounter_ip'] =None
#     saved_ip=None
#     time_posted = request.session.get('tools_Download_time')
#     savedTimeInSession=None
#     time_diff=0


#     # data=datetime.now()
#     # print("time",type(data))
#     # data1=json.dumps(data, default=json_util.default)
#     # aList =json.loads(data1)
#     # testdata=aList['$date']
#     # print("ourtest",aList['$date'])
#     # print("datatatataa",type(datetime.fromisoformat(testdata[:-1])))
#     # timetobesave=datetime.fromisoformat(testdata[:-1])
#     # print("timetoionebnfftdgbkki",timetobesave)
#     # print("timetoionebnfftdgbkki-TYpe",type(timetobesave))


#     if time_posted is not None:
#         print("time_posted not none")
#         print(time_posted)
#         print("datatatataa",type(datetime.fromisoformat(time_posted[:-1])))
#         savedTimeInSession=datetime.fromisoformat(time_posted[:-1])
#         dataCurrentTime=datetime.now()
#         print("time",type(dataCurrentTime))
#         # dataCurrent1=json.dumps(dataCurrent, default=json_util.default)
#         # aListdataCurrent1=json.loads(dataCurrent1)
#         # testdata3=aListdataCurrent1['$date']
#         # print("datatestsaved",savedTime)
#         timediff = dataCurrentTime - savedTimeInSession
#         time_diff = timediff.total_seconds()
#         print("timediff",timediff.total_seconds())
#     else:
#         print("time_posted none")
#     print("saved_ip",saved_ip)

#     if time_diff < 20:
#         saved_ip=request.session.get('toolsDownloadCounter_ip')
#     else:
#         request.session['toolsDownloadCounter_ip'] =None

#     if savedTimeInSession is not None:
#         print("savedTimeInSession inside second not none")
#         if ip != saved_ip:
#             print("ip is defferent inside second not none")
#             # if time_diff < 10:
#             print("time is less than 10 seconds inside second not none")
#             request.session['toolsDownloadCounter_ip'] = ip
#             data=datetime.now()
#             print("time",type(data))
#             data1=json.dumps(data, default=json_util.default)
#             aList =json.loads(data1)
#             testdata=aList['$date']
#             request.session['tools_Download_time'] = testdata
#             print("increase download count second")
#             tool_obj = ToolsData.objects.get(pk=id)
#             print("tools_obje",tool_obj)
#             print("before",tool_obj.ToolsData_DownloadCounter)
#             tool_obj.ToolsData_DownloadCounter= tool_obj.ToolsData_DownloadCounter + 1
#             tool_obj.save()
#             print("after",tool_obj.ToolsData_DownloadCounter)
#             return redirect('Localisation_App:toolsPage')
#             # else:
#             #     print("time is more than 10 seconds inside second not none")
#             #     request.session['toolsDownloadCounter_ip'] = ip
#             #     data=datetime.now()
#             #     print("time",type(data))
#             #     data1=json.dumps(data, default=json_util.default)
#             #     aList =json.loads(data1)
#             #     testdata=aList['$date']
#             #     request.session['tools_Download_time'] = testdata
#             #     return redirect('Localisation_App:toolsPage')
#         else:
#             print("ip is same inside second not none")
#             request.session['toolsDownloadCounter_ip'] = ip
#             data=datetime.now()
#             print("time",type(data))
#             data1=json.dumps(data, default=json_util.default)
#             aList =json.loads(data1)
#             testdata=aList['$date']
#             request.session['tools_Download_time'] = testdata
#             return redirect('Localisation_App:toolsPage')
#     else:
#         print("savedTimeInSession inside second none")
#         if ip != saved_ip:
#             print("ip is defferent inside second none")
#             # if time_diff < 10:
#             print("time is less than 10 seconds inside second none")
#             request.session['toolsDownloadCounter_ip'] = ip
#             data=datetime.now()
#             print("time",type(data))
#             data1=json.dumps(data, default=json_util.default)
#             aList =json.loads(data1)
#             testdata=aList['$date']
#             request.session['tools_Download_time'] = testdata
#             print("increase download count second")
#             print("getcookie",request.session.get('toolsDownloadCounter_ip'))
#             tool_obj = ToolsData.objects.get(pk=id)
#             print("tools_obje",tool_obj)
#             print("before",tool_obj.ToolsData_DownloadCounter)
#             tool_obj.ToolsData_DownloadCounter= tool_obj.ToolsData_DownloadCounter + 1
#             tool_obj.save()
#             print("after",tool_obj.ToolsData_DownloadCounter)
#             return redirect('Localisation_App:toolsPage')
#             # else:
#             #     print("time is more than 10 seconds inside second none")
#             #     request.session['toolsDownloadCounter_ip'] = ip
#             #     print("Inside 300 seconds")
#             #     data=datetime.now()
#             #     print("time",type(data))
#             #     data1=json.dumps(data, default=json_util.default)
#             #     aList =json.loads(data1)
#             #     print("data343434",aList)
#             #     testdata=aList['$date']
#             #     request.session['tools_Download_time'] = testdata
#             #     return redirect('Localisation_App:toolsPage')
#         else:
#             print("ip is same inside second none")
#             request.session['toolsDownloadCounter_ip'] = ip
#             print("same and none ip first")
#             data=datetime.now()
#             print("time",type(data))
#             data1=json.dumps(data, default=json_util.default)
#             aList =json.loads(data1)
#             print("data343434",aList)
#             testdata=aList['$date']
#             request.session['tools_Download_time'] = testdata
#             print("inside second none")
#             return redirect('Localisation_App:toolsPage')


# Resources Page


def resourcesPage(request):
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
    resource_searchData = resource_title.replace(" ", "-")
    print("titlenone", resource_title)
    print("replace space ", resource_title.replace(" ", "-"))

    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    resoucesCategory_data = Resources_Category.objects.all()
    resources_Data = ResourceData.objects.all()
    count = ResourceData.objects.all().count()

    if request.method == "POST":
        print("insideSearchMethod")
        print(resource_searchData)
        resource_searchData12 = request.POST.get("resourcename")
        print("resourcestitle", resource_searchData12)
        resource_searchData1 = resource_searchData12.replace(" ", "-")

        if resource_searchData1 != '':
            resource_Data = ResourceData.objects.filter(
                ResourceData_slug__icontains=resource_searchData1)
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
                'resource_title': resource_searchData1,
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
    if resource_searchData != 'none':
        resource_Data1 = ResourceData.objects.filter(
            ResourceData_slug__icontains=resource_searchData)
        page = Paginator(resource_Data1, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = resource_Data1.count()
        print("hereee", resource_Data1)
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'resoucesdata': resource_Data1,
            'resource_title': resource_searchData,
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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


def resourceDownloadCounter(request, id):
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
    savedTimeInSession = None
    time_diff = 0
    if time_posted is not None:
        print("time_posted not none")
        print(time_posted)
        print("datatatataa", type(datetime.fromisoformat(time_posted[:-1])))
        savedTimeInSession = datetime.fromisoformat(time_posted[:-1])
        dataCurrentTime = datetime.now()
        print("time", type(dataCurrentTime))
        timediff = dataCurrentTime - savedTimeInSession
        time_diff = timediff.total_seconds()
        print("timediff", timediff.total_seconds())
    else:
        print("time_posted none")
    print("saved_ip", saved_ip)

    if time_diff < 60:
        saved_ip = request.session.get('resourcesDownloadCounter_ip')
    else:
        request.session['resourcesDownloadCounter_ip'] = None

    if ip != saved_ip:
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
        print("after", resources_obj.ResourceData_DownloadCounter)
        return redirect('Localisation_App:resourcesPage')
        # else:
        #     print("ip is same inside second not none")
        #     request.session['resourcesDownloadCounter_ip'] = ip
        #     data=datetime.now()
        #     print("time",type(data))
        #     data1=json.dumps(data, default=json_util.default)
        #     aList =json.loads(data1)
        #     testdata=aList['$date']
        #     request.session['resources_Download_time'] = testdata
        #     return redirect('Localisation_App:resourcesPage')
    else:
        # print("savedTimeInSession inside second none")
        # if ip != saved_ip:
        # print("ip is defferent inside second none")
        # # if time_diff < 10:
        # print("time is less than 10 seconds inside second none")
        # request.session['resourcesDownloadCounter_ip'] = ip
        # data=datetime.now()
        # print("time",type(data))
        # data1=json.dumps(data, default=json_util.default)
        # aList =json.loads(data1)
        # testdata=aList['$date']
        # request.session['resources_Download_time'] = testdata
        # print("increase download count second")
        # print("getcookie",request.session.get('resourcesDownloadCounter_ip'))
        # resources_obj = ResourceData.objects.get(pk=id)
        # print("resources_obje",resources_obj)
        # print("before",resources_obj.ResourceData_DownloadCounter)
        # resources_obj.ResourceData_DownloadCounter= resources_obj.ResourceData_DownloadCounter + 1
        # resources_obj.save()
        # print("after",resources_obj.ResourceData_DownloadCounter)
        # return redirect('Localisation_App:resourcesPage')
        # else:
        print("ip is same inside second none")
        request.session['resourcesDownloadCounter_ip'] = ip
        print("same and none ip first")
        data = datetime.now()
        print("time", type(data))
        data1 = json.dumps(data, default=json_util.default)
        aList = json.loads(data1)
        print("data343434", aList)
        testdata = aList['$date']
        request.session['resources_Download_time'] = testdata
        print("inside second none")
        return redirect('Localisation_App:resourcesPage')


# Successstory Page
def successstoryPage(request):
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
    story_searchData = story_title.replace(" ", "-")
    print("titlenone", story_title)
    print("replace space ", story_title.replace(" ", "-"))
    print("titlenone", story_title)
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    successStories_CategoryData = SuccessStories_Category.objects.order_by(
        'SuccessStories_Cat_Priority')
    successStoriesData = SuccessStories.objects.all().order_by('SuccessStories_Priority')

    if request.method == "POST":
        print("insideSearchMethod")
        print(story_title)

        story_searchData12 = request.POST.get("storyname")
        print("resourcestitle", story_searchData12)
        story_searchData1 = story_searchData12.replace(" ", "-")

        if story_searchData1 != '':
            successStoriesData = SuccessStories.objects.filter(
                SuccessStories_slug__icontains=story_searchData1).order_by('SuccessStories_Priority')
            count = successStoriesData.count()
            print("dataStoriesdssds", count)
            page = Paginator(successStoriesData, 8)
            page_list = request.GET.get('page')
            # print("pagenumber",page_list)
            page = page.get_page(page_list)
            context = {
                'topmenus': TopMenuItemsdata,
                'FooterMenuItemsdata': FooterMenuItemsdata,
                'story_title': story_searchData1,
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
    if story_searchData != 'none':
        Stories_Data1 = SuccessStories.objects.filter(
            SuccessStories_slug__icontains=story_searchData).order_by('SuccessStories_Priority')
        page = Paginator(Stories_Data1, 8)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        count = Stories_Data1.count()
        print("hereee", Stories_Data1)
        context = {
            'topmenus': TopMenuItemsdata,
            'FooterMenuItemsdata': FooterMenuItemsdata,
            'SuccessStoriesData': Stories_Data1,
            'story_title': story_searchData,
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    if request.method == "POST":
        nameodservice = request.POST.get("nameodservice")
        print("nameeee", nameodservice)

    return render(request, 'Localisation_App/ServicesDemoPage.html')


def srvGoTranslateWebLocalizer(request):
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    return render(request, 'Localisation_App/ServicesDemoPage.html')


def srvOnscreenKeyboard(request):
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
                return render(request, 'Localisation_App/ttsService.html', context)

    context = {
        "service": "srvTTS",
        "TTS_Form": tTS_Form,
        "data": "srvTTS",
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        "DIVTITLE": "HELLO"
    }
    return render(request, 'Localisation_App/ttsService.html', context)


def srvTransliteration(request):
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    return render(request, 'Localisation_App/transliteration_modal.html', context)


# Faqs Page
def faqs(request):
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
    logger.info("INSIDE views of Contact us ")
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    footer_sub_data = Footer_Links_Info.objects.all().filter(
        Footer_Links_Info_MainTitle__Footer_Links_Title__contains="help")
    TopMenuItemsdata = TopMenuItems.objects.all()
    num = random.randrange(1121, 9899)
    logger.info("random num generated for captcha in contact us page")
    str_num = str(num)
    context = {
        'FooterMenuItemsdata': FooterMenuItemsdata,
        'footer_sub_data': footer_sub_data,
        'topmenus': TopMenuItemsdata,
        'img': str_num
    }
    logger.error("context assigned values in contact us views..........")

    return render(request, 'Localisation_App/contactus.html', context)


def submit(request, img):
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
    url = request.session.get('requested_url')
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
                print("second method called")
                login(request, user)
                return redirect('Localisation_App:'+url)
            else:
                messages.error(request, 'Wrong Username or password')
                return redirect('Localisation_App:login')

        else:
            messages.error(
                request, 'Error Processing Your Request,Wrong Username or password ')
            return redirect('Localisation_App:login')
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


def changePassword(request, token):
    form = UserChangePasswordForm()
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
                if password1 == password2:
                    if user_id is None:
                        messages.error(request, 'User Not Found')
                        return redirect('http://127.0.0.1:5555/changePassword/'+token)
                    else:
                        user_Register_obj = UserRegistration.objects.get(
                            pk=user_id)
                        user_Register_obj.userregistration_password = password1
                        user_Register_obj.userregistration_confirm_password = password2
                        user_Register_obj.save()

                        user_main_obj = User.objects.get(
                            username=user_Profile_obj.userregistration_username)
                        user_main_obj.set_password(password1)
                        user_main_obj.save()
                        messages.success(
                            request, 'Password Reset Successfully')
                        print('Password Reset Successfully ')
                        return redirect('http://127.0.0.1:5555/changePassword/'+token)
                else:
                    messages.error(request, 'Passwords are not matching')
                    return redirect('http://127.0.0.1:5555/changePassword/'+token)
            else:
                messages.error(request, 'Data is not valid')
                return redirect('http://127.0.0.1:5555/changePassword/'+token)
        else:
            user_id = user_Profile_obj.pk
            context = {
                'form': form,
                'User_Id': user_id
            }
            messages.error(request, '')
            return render(request, 'Localisation_App/changePassword.html', context)
    else:
        messages.success(request, 'User Not Found')
        print('User Not Found')
        return redirect('http://127.0.0.1:5555/changePassword/'+token)


def forgetPassword(request):
    form = UserForgetPasswordForm()
    try:
        if request.method == 'POST':
            form = UserForgetPasswordForm(data=request.POST)
            if form.is_valid():
                print('insideValidmethod')
                username = form.cleaned_data['username']
                if not User.objects.filter(username=username).first():
                    messages.error(
                        request, 'No user found with this username')
                    print('No user found with this username')
                    return redirect('Localisation_App:forgetPassword')
                else:
                    print('user is not none')
                    user_obj = User.objects.get(username=username)
                    token = str(uuid.uuid4())
                    user_Profile_obj = UserRegistration.objects.get(
                        userregistration_username=username)
                    user_Profile_obj.userregistration_token = token
                    user_Profile_obj.save()

                    mail_send_status = send_forget_password_email(
                        user_Profile_obj.userregistration_email_field, token)
                    print("userdata", user_obj)
                    print("mail_send_status", mail_send_status)
                    if mail_send_status:
                        messages.success(
                            request, 'An email is sent on your registered Email-Id')
                        print('An email is sent')
                        return redirect('Localisation_App:forgetPassword')
                    else:
                        messages.error(request, 'Failed to send sn email')
                        print('Failed to send sn email')
                        return redirect('Localisation_App:forgetPassword')
            else:
                messages.error(request, 'Data is not valid')
                return redirect('Localisation_App:forgetPassword')
    except Exception as e:
        print(e)
    messages.error(request, '')
    context = {
        'form': form
    }
    return render(request, 'Localisation_App/forgetPassword.html', context)


def goTranslate(request):
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    context = {
        'topmenus': TopMenuItemsdata,
        'FooterMenuItemsdata': FooterMenuItemsdata,
        "service": "goTranslate"
    }
    return render(request, 'Localisation_App/ServicesDemoPage.html', context)


def dashboard(request):
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
    TopMenuItemsdata = TopMenuItems.objects.all()
    FooterMenuItemsdata = FooterMenuItems.objects.all()
    Total_Tools_DownloadCount = ToolsData.objects.aggregate(
        Sum('ToolsData_DownloadCounter'))
    # print(Total_Tools_DownloadCount)
    # print(type(Total_Tools_DownloadCount))

    Total_ResourceData_DownloadCount = ResourceData.objects.aggregate(
        Sum('ResourceData_DownloadCounter'))
    # print(Total_ResourceData_DownloadCount)
    # print(type(Total_ResourceData_DownloadCount))

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
        'resourcesHitCount': resourcesName_hitCount_Per_Name,
        'Total_Tools_DownloadCount': Total_Tools_DownloadCount,
        'Total_ResourceData_DownloadCount': Total_ResourceData_DownloadCount

    }
    return render(request, 'Localisation_App/dashboard.html', context)


# Translation Quote
@login_required()
def translation_quote(request):
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
        company_email = request.POST.get('company_email')
        language = request.POST.get('language')
        domain = request.POST.get('domain')
        delivery_date = request.POST.get('delivery_date')
        client_remark = request.POST.get('client_remark')

        form = TranslationQuoteForm(request.POST)

        context['form'] = form
        print("dsnghufdygiu")
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

            # generate application number (UNIQUE)
            #

            application_number = str('GI-' + str(date.today().year) + '-' +
                                     current_user.username[0:2].upper() + str(random.randrange(100000000, 1000000000)))
            print("application ", application_number)

            data = TranslationQuote(
                url=url, company_email=company_email, language=language, domain=domain, delivery_date=delivery_date, client_remark=client_remark, application_number=application_number, username=current_user)
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
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
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
        # print(data["percentage"])
        guidelinesCount_Per_Type.append(data["percentage"])

    for n in tools_data:
        id.append(n.id)
    # print(id)
    for n in id:
        # print(n)
        data = ToolsData.objects.values('ToolsData_DownloadCounter').get(id=n)
        # print(data)
        # print(data["ToolsData_DownloadCounter"])
        toolsName_hitCount_Per_Name.append(data["ToolsData_DownloadCounter"])

    for n in id:
        datname = ToolsData.objects.values('ToolsData_HeadingName').get(id=n)
        toolsName.append(datname["ToolsData_HeadingName"])
        # print(datname["ToolsData_HeadingName"])

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

    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
    top_menu_items_data = TopMenuItems.objects.all()
    footer_menu_items_data = FooterMenuItems.objects.all()
    context = {
        'topmenus': top_menu_items_data,
        'FooterMenuItemsdata': footer_menu_items_data

    }

    return render(request, 'Localisation_App/machine_translation.html', context)


def name_matcher(request):
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
    top_menu_items_data = TopMenuItems.objects.all()
    footer_menu_items_data = FooterMenuItems.objects.all()
    context = {
        'topmenus': top_menu_items_data,
        'FooterMenuItemsdata': footer_menu_items_data,


    }

    return render(request, 'Localisation_App/name_matcher.html', context)


def empanelled_agencies(request):
    url = resolve(request.path_info).url_name
    request.session['requested_url'] = url
    top_menu_items_data = TopMenuItems.objects.all()
    footer_menu_items_data = FooterMenuItems.objects.all()

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
    return render(request, 'Localisation_App/empanelled_agencies.html', context)


# translation_quote_user_dashboard
@login_required
def translation_quote_user_dashboard(request):
    top_menu_items_data = TopMenuItems.objects.all()
    footer_menu_items_data = FooterMenuItems.objects.all()

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
    return render(request, 'Localisation_App/translation_quote_user_dashboard.html', context)


# translation_quote_show
@login_required
def translation_quote_show(request, application_number):
    # print("application number ", application_number)
    top_menu_items_data = TopMenuItems.objects.all()
    footer_menu_items_data = FooterMenuItems.objects.all()

    translation_quote_data = TranslationQuote.objects.filter(
        application_number=application_number)[0]
    print(translation_quote_data)
    username = translation_quote_data.username

    print(username.username)

    user_details = UserRegistration.objects.filter(
        userregistration_username=username.username)

    context = {
        'topmenus': top_menu_items_data,
        'FooterMenuItemsdata': footer_menu_items_data,
        'translation_quote_data': translation_quote_data,
        'user_details': user_details,
    }
    return render(request, 'Localisation_App/translation_quote_show.html', context)
