from datetime import datetime
from django.contrib.auth import authenticate,logout, login
from django.http import Http404, HttpResponseRedirect, JsonResponse,HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
import requests, json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from reportlab.pdfgen import canvas
import io
from reportlab.lib.colors import blue, gray, whitesmoke,white,black
from reportlab.lib.units import inch
from django.contrib.auth.decorators import login_required
from uis.models import *
from ..import uis_pdf
from django.db.models import ProtectedError, RestrictedError
import pandas as pd
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
from django.db.models import Value
from django.db.models.functions import Substr


root = "http://173.10.2.108:9092/"
# root = "http://172.22.10.11:9091/"
cashop_api = root + "api/cashop/lookup"
login_api = root + "api/login"
cashop_api_ecntr = root + "api/cashop/encounter"
malasakit_patiet_details = root + "api/malasakit/patient-details"
malasakit_api_showRCD= root + "api/cashop/showRCD"
malasakit_api_adm_patient = root + "api/adm/admlist"
def auth_login(request):
    if request.session.get('employee_id') is None:
        if request.method == 'POST':
            userid = request.POST.get("userid").upper()
            password = request.POST.get("password")
            login_response = requests.post(login_api, data={'username': userid, 'password': password})
            login_json_response = login_response.json()

            if login_json_response['status'] == 'success':
                if json.dumps(login_json_response['data']) == "[]":
                    messages.warning(request, "Invalid Username or Password")  
                    return render(request, 'auth-login.html')
                else:
                    request.session['employee_id'] = login_json_response['data'][0]['employeeid']
                    request.session['user_level'] = login_json_response['data'][0]['user_level']
                    request.session['name'] = login_json_response['data'][0]['name']
                    request.session['position'] = login_json_response['data'][0]['postitle']
                    request.session['contactno'] = login_json_response['data'][0]['contactno']
                    request.session['email'] = login_json_response['data'][0]['email']
                    request.session['userid'] = userid
                    if login_json_response['data'][0]['user_level'] == 1:#ADMIN
                        return HttpResponseRedirect('/')
                    # elif login_json_response['data'][0]['user_level'] == 15:#BILLING
                    #     return HttpResponseRedirect('/')
                    # elif login_json_response['data'][0]['user_level'] == 3:#LABORATORY
                    #     return HttpResponseRedirect('/')
                    # elif login_json_response['data'][0]['user_level'] == 4:#RADIOLOGY
                    #     return HttpResponseRedirect('/')
                    # elif login_json_response['data'][0]['user_level'] == 5:#PHARMACY
                    #     return HttpResponseRedirect('/')
                    # elif login_json_response['data'][0]['user_level'] == 6:#PHILHEATH
                    #     return HttpResponseRedirect('/')
                    # elif login_json_response['data'][0]['user_level'] == 16:#CASHIERING
                    #     return HttpResponseRedirect('index')
                    # elif login_json_response['data'][0]['user_level'] == 2:#NURSING
                    #     return HttpResponseRedirect('/')
                    # elif login_json_response['data'][0]['user_level'] == 11:#CSSR
                    #     return HttpResponseRedirect('/')
                    else:
                        messages.error(request, "Access Denied! Please contact the system administrator")
                        return render(request, 'auth-login.html')
            else:
                messages.warning(request, "Invalid Username or Password")  
                return render(request, 'auth-login.html')

        else:
            return render(request, 'auth-login.html')
    else:
        return HttpResponseRedirect('/')
def sign_out(request):
    logout(request)
    messages.success(request, 'Successfully Logged-out in!')
    return HttpResponseRedirect("/auth_login")

def dashboard(request):
    if request.session.get('employee_id') is not None:
        
        uis_count = 0
        mssat_count = 0
        scsr_count=0
        now = datetime.now()
        date_today = datetime.strftime(now, '%Y-%m-%d')
        uis_count = UIS.objects.filter(date=date_today).count()
        uis = UIS.objects.all().order_by('-date')
        asst_amt={}
        patient_uis = IdentifyingInformation.objects.all()

        mssat_count = MSSAT.objects.filter(doac=date_today).count()
        for u in uis:
            uis_misc = UIS_misc.objects.filter(uis=u.uis)
            for i in uis_misc:
                
                asst_amt_init = float(i.total_amount_of_assistance)
                date_init =  datetime.strptime(i.uis.date, '%Y-%m-%d')
                i.uis.date = date_init.strftime("%B %d, %Y")
                if i.uis.date in asst_amt:
                    asst_amt[i.uis.date] += round(asst_amt_init,2)
                else:
                    asst_amt[i.uis.date] = round(asst_amt_init,2)
        return render(request, 'uis/dashboard.html',{'asst_amt':asst_amt.items(),'uis':uis,'patient_uis':patient_uis,'mssat_count':mssat_count,'uis_count':uis_count,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")

def home(request):
    if request.session.get('employee_id') is not None:
        if 'complain' in request.session:
            del request.session['complain']
        getData = ""
        if request.method == 'POST':
            search_text = request.POST.get('data-input','')
            if search_text:
                results = requests.post(cashop_api,data = {'hospno': search_text}).json()
                now = datetime.now()
                time_started = datetime.strftime(now, '%I:%M:%S %p')
                request.session['start_time'] = time_started
                if results['status'] == 'success':
                    getData = results['data']
                    if getData == []:
                        results = requests.post(cashop_api,data = {'lastname': search_text}).json()
                        getData = results['data']
            else:
                getData =[]
                
        return render(request, 'uis/patient_search.html',{'data':getData,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")
def uis_list(request):
    query = request.GET.get('search', '')
    if query:
        uis_show = UIS.objects.all()
        show = IdentifyingInformation.objects.filter(Q (client_name__icontains=query))
    else:
        uis_show = UIS.objects.all()
        show = IdentifyingInformation.objects.all()[:10]
    return render(request,'uis/uis_list.html',{'user_id':request.session['userid'],'show':show,'uis':uis_show,'user':request.session['name']})

def mss_tool_list(request):
    query = request.GET.get('search', '')
    if query:
        uis_show = UIS.objects.all()
        show = IdentifyingInformation.objects.filter(Q (client_name__icontains=query))
        mssat_uis = MSSAT.objects.all()
    else:
        uis_show = UIS.objects.all()
        show = IdentifyingInformation.objects.all()[:10]
        mssat_uis = MSSAT.objects.all()
    return render(request,'uis/mss_tool_list.html',{'show':show,'uis':uis_show,'mssat_uis':mssat_uis,'user':request.session['name']})

def admitted_list(request):
    show_admlist = requests.post(malasakit_api_adm_patient).json()
    now = datetime.now()
    uis = UIS.objects.all()
    time_started = datetime.strftime(now, '%I:%M:%S %p')
    request.session['start_time'] = time_started
    adm = "ADM"
    if show_admlist['status'] == 'success':
        get_adm_patient = show_admlist['data']
        request.session['complain'] = 'ADMITTED'
        for i in get_adm_patient:
            i['enccode'] = i['enccode'].replace("/","-")
    else:
        get_adm_patient = []
    return render(request,'uis/admited_patient.html',{'uis':uis,'adm':adm,'adm_patient':get_adm_patient,'user':request.session['name']})
def get_patient_enctr(request,hospno):
    if request.session.get('employee_id') is not None:
        enccode = ''
        getPatientEnctrs = requests.post(cashop_api_ecntr,data = {'hospno': hospno}).json()
        results = requests.post(cashop_api,data = {'hospno': hospno}).json()
        get_results_name = results['data']
        for ii in get_results_name:
            fullname = ii['patfirst']+" "+ii['patmiddle']+" "+ii['patlast']
        if getPatientEnctrs['status'] == 'success':
            getPatientData = getPatientEnctrs['data']
            for c in getPatientData:
                c['enccode'] = c['enccode'].replace("/","-")
                enccode = c['enccode']
                timestamp_str = c['encdate']
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                c['encdate'] = timestamp.strftime("%B %d, %Y")
        else:
            messages.success(request, 'Patient has no Data!')
            return HttpResponseRedirect("/")
        return render(request, 'uis/date_to_charge.html',{'code':enccode,'enctrData':getPatientData, 'hospno':hospno,'fullname':fullname,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")
def report(request):
    d = datetime.now()
    date_today = datetime.strftime(d, '%Y-%m-%d')
    u =None
    n=None
    h=None
    k=None
    r=None
    if request.method == "POST":
        d1 = request.POST.get('d1')
        d2 = request.POST.get('d2')
        user = request.POST.get('user')
        try:
            if user:
                n = UIS_misc.objects.filter(swo = user)
                for y in n:
                    if y.swo == request.session['name']:
                        u = UIS.objects.filter(date__lte = d2,date__gte =d1, uis = y.uis_id)
                        h = IdentifyingInformation.objects.filter(uis = y.uis_id) 
                        k = Informant.objects.filter(uis = y.uis_id) 
                        r = Recommendations.objects.filter(uis=y.uis_id,uis_misc = y.uis_misc)
                    else:
                        h = ""    
        except:
            u =None
        return render(request,'uis/reports.html',{'date_today':date_today,'k':k,'r':r,'n':n,'h':h,'u':u,'d':d,'user_id':request.session['userid'],'user':request.session['name']})   
    else:
        return render(request,'uis/reports.html',{'date_today':date_today,'k':k,'r':r,'n':n,'h':h,'u':u,'d':d,'user_id':request.session['userid'],'user':request.session['name']})