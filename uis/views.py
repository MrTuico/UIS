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
from . import uis_pdf
from django.db.models import ProtectedError, RestrictedError
import pandas as pd
from openpyxl.workbook import Workbook
from openpyxl import load_workbook


root = "http://173.10.2.108:9092/"
# root_test = "http://172.22.10.11:9091/"
cashop_api = root + "api/cashop/lookup"
login_api = root + "api/login"
cashop_api_ecntr = root + "api/cashop/encounter"
malasakit_patiet_details = root + "api/malasakit/patient-details"
malasakit_api_showRCD= root + "api/cashop/showRCD"

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
        uis = UIS.objects.filter(date=date_today)
        patient_uis = IdentifyingInformation.objects.all()
        for u in uis:
            mssat_count = MSSAT.objects.filter(uis_id=u.uis).count()
        return render(request, 'uis/dashboard.html',{'uis':uis,'patient_uis':patient_uis,'mssat_count':mssat_count,'uis_count':uis_count,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")

def home(request):
    if request.session.get('employee_id') is not None:
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


def get_patient_enctr(request,hospno):
    if request.session.get('employee_id') is not None:
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
        return render(request, 'uis/date_to_charge.html',{'code':enccode,'enctrData':getPatientData, 'hospno':hospno,'fullname':fullname,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")
def add_uis(request, hospno,code, toecode):
    if request.session.get('employee_id') is not None:
        # print(request.session['start_time'])
        now = datetime.now()
        complain = ""
        date_today = datetime.strftime(now, '%Y-%m-%d')
        date_show = datetime.strftime(now, '%b %d, %Y')
        time_show = request.session['start_time']
        time_ended = datetime.strftime(now, '%I:%M %p')
        # time_show = datetime.strftime(now, '%h-%i-%d')
        mms_no_auto = datetime.strftime(now, '%Y-%m-')
        showRCD = requests.post(malasakit_api_showRCD).json()
        if showRCD['status'] == 'success':
            get_rcd  = showRCD['data']
        results = requests.post(malasakit_patiet_details,data = {'enccode': code}).json()
        if results['status'] == 'success':
            get_result = results['data']['details']
            get_complaint = results['data']['complaint']
            try:
                get_address = results['data']['address']
            except KeyError:
                get_address = 'N/A'
            for cc in get_complaint:
                complain = cc['history']
            for ii in get_result:
                if ii['patsuffix'] is None:
                    suffix = ''
                else:
                    suffix = ii['patsuffix']
                fullname = ii['patlast']+", "+ii['patfirst']+" "+ii['patmiddle']+" "+suffix
                if ii['patsex'] == 'M':
                    gender='MALE'
                else:
                    gender = 'FEMALE'
                bday = ii['patbdate']
                bdate = datetime.fromisoformat(bday[:-1])
                # bdate= datetime.strftime(bday_init, '%Y/%m/%d')
                
                def calculate_age(birth_date):
                    today = datetime.today()
                    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                    return age
                age = calculate_age(bdate)
                pob = ii['patbplace']
                occu = ii['patempstat']
                if ii['patcstat'] == 'C':
                    cstat='CHILD'
                elif ii['patcstat'] == 'D':
                    cstat = 'DIVORSED'
                elif ii['patcstat'] == 'M':
                    cstat = 'MARRIED'
                elif ii['patcstat'] == 'X':
                    cstat = 'SEPARATED'
                elif ii['patcstat'] == 'S':
                    cstat = 'SINGLE'
                elif ii['patcstat'] == 'W':
                    cstat = 'WIDOW/WIDOWER'
                else:
                    cstat = 'NONE'
                if ii['natcode'] == 'FILIP':
                    nat = 'FILIPINO'
                else:
                    nat= 'OTHERS'
                if ii['relcode'] == 'CATHO':
                    rel = 'ROMAN CATHOLIC'
                else:
                    rel = 'OTHERS'
                
                # age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

            if request.method == 'POST':
                date_today = datetime.strftime(now, '%Y-%m-%d')
                time_today =request.session['start_time']
                time_end = datetime.strftime(now,'%I:%M %p')
    
                #informant data
                noi = request.POST.get('noi').upper()
                rtp = request.POST.get('rtp').upper()
                cnums = request.POST.get('cnums')
                pa = request.POST.get('pa').upper()
                tot_income = request.POST.get('tot_income')
                tot_expense = request.POST.get('tot_expense')
                category = request.POST.get('klass')
                house_size = request.POST.get('housize')
                f_hsize = int(house_size) + 1
                phil_no = request.POST.get('phil_no')

                uis_add = UIS(date = date_today,hospno = hospno,phil_no=phil_no,total_income = tot_income,total_expense = tot_expense,category=category,householdsize = f_hsize)
                uis_add.save()
                if uis_add.uis:
                    uis_id = UIS.objects.get(uis = uis_add.uis)
                    # informant
                    a = Informant(uis=uis_id,date_of_intake = date_today,time_of_interview=time_today,end_time_of_interview=time_end,fullname=noi,relation_to_patient = rtp,contact_number = cnums,address = pa)
                    a.save()
                    
                    #identifying information
                    cn = request.POST.get('cn')
                    sx = request.POST.get('gender')
                    bdey = request.POST.get('bdate')
                    age = request.POST.get('age')
                    cs = request.POST.get('cs')
                    rel = request.POST.get('rel')
                    nat = request.POST.get('nat')
                    hea = request.POST.get('hea')
                    occu = request.POST.get('occu')
                    mi = request.POST.get('mi')
                    pt = request.POST.get('pt')
                    pob = request.POST.get('pob')
                    pea = request.POST.get('pea')
                    pra = request.POST.get('pra')
                    b = IdentifyingInformation(uis=uis_id,client_name = cn,gender=sx,dob = bdey,age=age,cstat = cs,religion = rel,nationality = nat,hea=hea,occupation = occu,mi=mi,patient_type=pt,pob=pob,permanent_address=pea,present_address=pra)
                    b.save()

                     #family composition
                    fam_com = request.POST.get('familycom')
                  
                    if fam_com:
                        fam_data = json.loads(fam_com)
                        for f in fam_data:
                            cname = f['cname']
                            fcgender = f['gender']
                            fccstat = f['cstat']
                            fcrtp = f['rtp']
                            fchea = f['hea']
                            fcoccu = f['occu']
                            fcmi = f['mi']
                            fcage = f['fage']
                            c = FamilyComposition(uis=uis_id,fullname = cname,gender=fcgender,cstat = fccstat,relation_to_patient = fcrtp,hea=fchea,occupation=fcoccu,mi=fcmi,age=fcage)
                            c.save()
                            fc_id = FamilyComposition.objects.get(familyComposition = c.familyComposition)
                    elif fam_com == '' or fam_com is None:
                        c = FamilyComposition(uis=uis_id,fullname = cn,gender=sx,cstat = cs,relation_to_patient = "SELF", hea=hea,occupation=occu,mi=mi,age=age)
                        c.save()
                        fc_id = FamilyComposition.objects.get(familyComposition = c.familyComposition)
                    else:
                        fam_data = []
                    fam_com_osof = request.POST.get('familycomosof')
                    if fam_com_osof:
                        famosof_data = json.loads(fam_com_osof)
                        for y in famosof_data:
                            desc_osof = y['desc_osof']
                            amt_osof = y['amt_osof']
                            x = Fc_other_source(uis=uis_id,familyComposition = fc_id,otherSources_of_fi_desc = desc_osof,otherSources_of_fi=amt_osof)
                            x.save()
                    else:
                        famosof_data = []

                     # #list of expenses
                    le_house = request.POST.get('le_house')
                    le_amt_house = request.POST.get('le_amt_house')
                    le_lot = request.POST.get('le_lot')
                    le_amt_lot =request.POST.get('le_amt_lot')
                    light_source = []
                    water_source = []
                    other_expenses = []
                    desc_light_source = []
                    desc_water_source = []
                    desc_others_expenses = []
                    prob_presented = []
                    prob_presented_desc=[]

                    elec = request.POST.get('elec', False)
                    amt_elec_init = request.POST.get('amt_elec')
                    kero = request.POST.get('kero', False)
                    amt_kero_init = request.POST.get('amt_kero')
                    cand = request.POST.get('cand', False)
                    amt_cand_init = request.POST.get('amt_cand')
                    oth = request.POST.get('oth', False)
                    amt_oth_init = request.POST.get('amt_oth')
                    if elec:
                        desc_elec = "ELECTRICITY"
                        amt_elec = float(amt_elec_init)
                    else:
                        desc_elec = ""
                        amt_elec = 0
                        pass
                    if kero:
                        desc_kero = "KEROSENE"
                        amt_kero = float(amt_kero_init)
                    else:
                        desc_kero = ""
                        amt_kero = 0
                        pass
                    if cand:
                        desc_cand = "CANDLE"
                        amt_cand = float(amt_cand_init)
                    else:
                        desc_cand = ""
                        amt_cand = 0
                        pass
                    if oth:
                        desc_oth = "OTHERS"
                        amt_oth = float(amt_oth_init)
                    else:
                        desc_oth = ""
                        amt_oth = 0
                    desc_light_source = [desc_elec,desc_kero,desc_cand,desc_oth]
                    light_source= [amt_elec,amt_kero,amt_cand,amt_oth]
                        
                    water_source_public = request.POST.get('pub', False)
                    amt_water_source_public_init = request.POST.get('amt_pub')
                    water_source_nat = request.POST.get('natu', False)
                    amt_water_source_nat_init = request.POST.get('amt_nat')
                    water_source_wd = request.POST.get('wd', False)
                    amt_water_source_wd_init = request.POST.get('amt_wd')
                    water_source_min = request.POST.get('min', False)
                    amt_water_source_min_init = request.POST.get('amt_min')
                    if water_source_public:
                        desc_public = "PUBLIC"
                        amt_water_source_public = float(amt_water_source_public_init) 
                    else:
                        desc_public = ""
                        amt_water_source_public = 0
                        pass
                    if water_source_nat:
                        desc_natural = "NATURAL"
                        amt_water_source_nat = float(amt_water_source_nat_init)
                    else:
                        desc_natural = ""
                        amt_water_source_nat = 0
                        pass
                    if water_source_wd:
                        desc_wd = "WATER DISTRICT"
                        amt_water_source_wd =  float(amt_water_source_wd_init)
                    else:
                        desc_wd = ""
                        amt_water_source_wd = 0
                        pass
                    if water_source_min:
                        desc_min = "MINERAL"
                        amt_water_source_min = float(amt_water_source_min_init)
                    else:
                        desc_min = ""
                        amt_water_source_min = 0
                    desc_water_source=[desc_public,desc_natural,desc_wd,desc_min]
                    water_source = [amt_water_source_public,amt_water_source_nat,amt_water_source_wd,amt_water_source_min]
                        
                    house = request.POST.get('house', False)
                    amt_house_init = request.POST.get('amt_house')
                    me = request.POST.get('me', False)
                    amt_me_init = request.POST.get('amt_me')
                    ip = request.POST.get('ip', False)
                    amt_ip_init = request.POST.get('amt_ip')
                    edu = request.POST.get('edu', False)
                    amt_edu_init = request.POST.get('amt_edu')
                    loan = request.POST.get('loan', False)
                    amt_loan_init = request.POST.get('amt_loan')
                    transpo = request.POST.get('transpo', False)
                    amt_transpo_init = request.POST.get('amt_transpo')
                    food = request.POST.get('food', False)
                    amt_food_init = request.POST.get('amt_food')
                    saving = request.POST.get('saving', False)
                    amt_saving_init = request.POST.get('amt_saving')
                    other = request.POST.get('other', False)
                    amt_other_init = request.POST.get('amt_other')
                    if house:
                        desc_house = "HOUSE"
                        amt_house = float(amt_house_init)
                    else:
                        desc_house = ""
                        amt_house = 0
                        pass
                    if me:
                        desc_me = "ME"
                        amt_me = float(amt_me_init)
                    else:
                        desc_me = ""
                        amt_me = 0
                        pass
                    if ip:
                        desc_ip = "IP"
                        amt_ip = float(amt_ip_init)
                    else:
                        desc_ip = ""
                        amt_ip = 0
                        pass
                    if edu:
                        desc_edu = "EDU"
                        amt_edu = float(amt_edu_init)
                    else:
                        desc_edu = ""
                        amt_edu = 0
                        pass
                    if loan:
                        desc_loan = "LOAN"
                        amt_loan = float(amt_loan_init)
                    else:
                        desc_loan = ""
                        amt_loan = 0
                        pass
                    if transpo:
                        desc_transpo = "TRANSPO"
                        amt_transpo = float(amt_transpo_init)
                    else:
                        desc_transpo = ""
                        amt_transpo = 0
                        pass
                    if food:
                        desc_food = "FOOD"
                        amt_food = float(amt_food_init)
                    else:
                        desc_food=""
                        amt_food = 0
                        pass
                    if saving:
                        desc_saving="SAVINGS"
                        amt_saving = float(amt_saving_init)
                    else:
                        desc_saving=""
                        amt_saving = 0
                        pass
                    if other:
                        desc_other = "OTHER"
                        amt_other = float(amt_other_init)
                    else:
                        desc_other = ""
                        amt_other = 0
                    desc_others_expenses = [desc_house,desc_me,desc_ip,desc_edu,desc_loan,desc_transpo,desc_food,desc_saving,desc_other]
                    other_expenses = [amt_house,amt_me,amt_ip,amt_edu,amt_loan,amt_transpo,amt_food,amt_saving,amt_other]
                    d = ListofExpenses(uis = uis_id, house = le_house,amt_house = le_amt_house,lot=le_lot,amt_lot=le_amt_lot,ligth_source=desc_light_source,amt_ligth_source = light_source,water_source=desc_water_source,amt_water_source = water_source,other_expenses=desc_others_expenses,amt_other_expenses = other_expenses)
                    d.save()

                    # # #problem Presented

                    hcop = request.POST.get('hcop', False)
                    hcop_desc = request.POST.get('hcop_desc')
                    fn = request.POST.get('fn', False)
                    fn_desc = request.POST.get('fn_desc')
                    emp = request.POST.get('emp', False)
                    emp_desc = request.POST.get('emp_desc')
                    ers = request.POST.get('ers', False)
                    ers_desc = request.POST.get('ers_desc')
                    hs = request.POST.get('hs', False)
                    hs_desc = request.POST.get('hs_desc')
                    osy = request.POST.get('osy', False)
                    osy_desc = request.POST.get('osy_desc')
                    if hcop:
                        n_hcop = "HCOP"
                        hcop_desc = hcop_desc
                    else:
                        n_hcop = ''
                        hcop_desc=''

                    if fn:
                        n_fn = "FN"
                        fn_desc = fn_desc
                    else:
                        n_fn = ''
                        fn_desc=''
                    if emp:
                        n_emp = "EMP"
                        emp_desc = emp_desc
                    else:
                        n_emp = ''
                        emp_desc=''
                    if ers:
                        n_ers = "ERS"
                        ers_desc = ers_desc
                    else:
                        n_ers=''
                        ers_desc=''
                    if hs:
                        n_hs = "HS"
                        hs_desc = hs_desc
                    else:
                        n_hs = ''
                        hs_desc=''
                    if osy:
                        n_osy = 'OSY'
                        osy_desc = osy_desc
                    else:
                        n_osy = ''
                        osy_desc=''
                    prob_presented = [n_hcop,n_fn,n_emp,n_ers,n_hs,n_osy]
                    prob_presented_desc = [hcop_desc,fn_desc,emp_desc,ers_desc,hs_desc,osy_desc]
                    e = ProblemPresented(uis = uis_id,problem= prob_presented,prob_desc = prob_presented_desc)
                    e.save()

                    #swa
                    swa = request.POST.get('swa')
                    f = SWA(uis = uis_id,swa_desc = swa)
                    f.save()

                    # reccomendations
                    reccomendations = request.POST.get('reccomdata')
                    if reccomendations:
                        reccom_data = json.loads(reccomendations)
                        for r in reccom_data:
                            mtoa = r['mtoa']
                            maos = r['maos']
                            mmoa = r['mmoa']
                            mfs = r['mfs']
                            g = Recommendations(uis = uis_id,type_of_assistance = mtoa,amt_of_assistance = maos,mode_of_assistance = mmoa,fund_source = mfs)
                            g.save()
                    else:
                        reccom_data = []
                    mssatcheck = request.POST.get('mssatcheck',False)
                    if mssatcheck:
                        fuel_src = []
                        amt_fuel_src = []
                        doac = request.POST.get('doac')
                        categorys = request.POST.get('categorys')
                        venue= request.POST.get('venue')
                        mss_no = request.POST.get('mss_no')
                        src_referal_name = request.POST.get('src_referal_name')
                        ward = request.POST.get('ward')
                        cnumba = request.POST.get('cnumba')
                        address = request.POST.get('address')
                        tla = request.POST.get('tla')
                        phil_mem = request.POST.get('phil_mem')
                        marginalized_sec_mem = request.POST.get('marginalized_sec_mem')
                        clothing_amt = request.POST.get('clothing_amt')
                        duration_of_prob = request.POST.get('duration_of_prob')
                        prev_treatment = request.POST.get('prev_treatment')
                        health_accessibility_prob = request.POST.get('health_accessibility_prob')
                        lpg = request.POST.get('lpg', False)
                        amt_lpg = request.POST.get('amt_lpg')
                        # elec = request.POST.get('elec', False)
                        # amt_elec = request.POST.get('m_amt_elec')
                        char = request.POST.get('char', False)
                        amt_char = request.POST.get('amt_char')
                        fwood = request.POST.get('fwood', False)
                        amt_fwood = request.POST.get('amt_fwood')
                        if lpg:
                            f_lpg = "LPG"
                            f_amt_lpg =float(amt_lpg)
                        else:
                            f_lpg = ""
                            f_amt_lpg = 0
                            pass
                        # if elec:
                        #     f_elec = "ELECTRICITY"
                        #     f_amt_elec =float(amt_elec)
                        # else:
                        #     f_elec = ""
                        #     f_amt_elec = 0
                        #     pass
                        if char:
                            f_char = "CHARCOAL"
                            f_amt_char =float(amt_char)
                        else:
                            f_char = ""
                            f_amt_char = 0
                            pass
                        if fwood:
                            f_fwood = "FIREWOOD"
                            f_amt_fwood =float(amt_fwood)
                        else:
                            f_fwood = ""
                            f_amt_fwood = 0
                        fuel_src = [f_lpg,f_char,f_fwood]
                        amt_fuel_src = [f_amt_lpg,f_amt_char,f_amt_fwood]
                        aa = MSSAT(uis=uis_id,doac = doac,venue=venue,category=categorys,basic_ward=ward,mss_no=mss_no,tla=tla,src_referal_name=src_referal_name,address=address,cnum=cnumba,phil_mem=phil_mem,marginalized_sec_mem=marginalized_sec_mem,fuel_source = fuel_src,amt_fuel_source = amt_fuel_src,clothing_amt=clothing_amt,duration_of_prob=duration_of_prob,prev_treatment=prev_treatment,health_accessibility_prob=health_accessibility_prob)
                        aa.save()
                    else:
                        mssatcheck = []
                        pass
                    
                    if mssatcheck:
                        upd_has_mssat = UIS.objects.get(uis = uis_add.uis)
                        upd_has_mssat.has_mssat = True
                        upd_has_mssat.save()
                        redirect_url_with_args = f'/{uis_id}/new_mssat_pdf'
                    else:
                        redirect_url_with_args = f'/{uis_id}/uis_pdf'
                    messages.success(request, "SUCCESSFULLY ADDED")
                    return redirect(redirect_url_with_args)

        return render(request, 'uis/add_uis.html',{'time_ended':time_ended,'time_show':time_show,'date_show':date_show,'get_rcd':get_rcd,'mms_no_auto':mms_no_auto,'date_today':date_today,'user':request.session['name'],'complain':complain,'toecode':toecode,'age':age,'rel':rel,'nat':nat,'cstat':cstat,'occu':occu,'address':get_address,'pob':pob,'code':code,'hospno':hospno,'fullname':fullname,'gender':gender,'bday':bdate})
    else:
        return HttpResponseRedirect("/auth_login")
def add_mssat(request, uis):
    if request.session.get('employee_id') is not None:
        now = datetime.now()
        date_today = datetime.strftime(now, '%Y-%m-%d')
        mms_no_auto = datetime.strftime(now, '%Y-%m-')
        uis_g = UIS.objects.get(uis=uis)
        time_starts = datetime.strftime(now, '%I:%M %p')
        request.session['mssat_start']= time_starts
        time_endede = datetime.strftime(now, '%I:%M %p')
        info_g = Informant.objects.get(uis=uis)
        if request.method == 'POST':
            fuel_src = []
            amt_fuel_src = []
            uis_id = UIS.objects.get(uis = uis)
            doac = request.POST.get('doac')
            categorys = request.POST.get('categorys')
            venue= request.POST.get('venue')
            mss_no = request.POST.get('mss_no')
            src_referal_name = request.POST.get('src_referal_name')
            ward = request.POST.get('ward')
            cnum = request.POST.get('cnum')
            address = request.POST.get('address')
            # employer = request.POST.get('employer')
            tla = request.POST.get('tla')
            phil_mem = request.POST.get('phil_mem')
            # mswd_cassif = request.POST.get('mswd_cassif')
            marginalized_sec_mem = request.POST.get('marginalized_sec_mem')
            clothing_amt = request.POST.get('clothing_amt')
            duration_of_prob = request.POST.get('duration_of_prob')
            prev_treatment = request.POST.get('prev_treatment')
            health_accessibility_prob = request.POST.get('health_accessibility_prob')
            lpg = request.POST.get('lpg', False)
            amt_lpg = request.POST.get('amt_lpg')
            # elec = request.POST.get('elec', False)
            # amt_elec = request.POST.get('amt_elec')
            char = request.POST.get('char', False)
            amt_char = request.POST.get('amt_char')
            fwood = request.POST.get('fwood', False)
            amt_fwood = request.POST.get('amt_fwood')
           

            if lpg:
                f_lpg = "LPG"
                f_amt_lpg =float(amt_lpg)
            else:
                f_lpg = ""
                f_amt_lpg = 0
                pass
            # if elec:
            #     f_elec = "ELECTRICITY"
            #     f_amt_elec =float(amt_elec)
            # else:
            #     f_elec = ""
            #     f_amt_elec = 0
            #     pass
            if char:
                f_char = "CHARCOAL"
                f_amt_char =float(amt_char)
            else:
                f_char = ""
                f_amt_char = 0
                pass
            if fwood:
                f_fwood = "FIREWOOD"
                f_amt_fwood =float(amt_fwood)
            else:
                f_fwood = ""
                f_amt_fwood = 0
            fuel_src = [f_lpg,f_char,f_fwood]
            amt_fuel_src = [f_amt_lpg,f_amt_char,f_amt_fwood]
            aa = MSSAT(uis=uis_id,doac = doac,venue=venue,category = categorys,basic_ward=ward,mss_no=mss_no,tla=tla,src_referal_name=src_referal_name,address=address,cnum=cnum,phil_mem=phil_mem,marginalized_sec_mem=marginalized_sec_mem,fuel_source = fuel_src,amt_fuel_source = amt_fuel_src,clothing_amt=clothing_amt,duration_of_prob=duration_of_prob,prev_treatment=prev_treatment,health_accessibility_prob=health_accessibility_prob)
            aa.save()
            upd_has_mssat = UIS.objects.get(uis = uis)
            upd_has_mssat.has_mssat = True
            upd_has_mssat.save()
            messages.success(request, "SUCCESSFULLY ADDED")
        return render(request, 'uis/new_add_mss_tool.html',{'time_start':request.session['mssat_start'],'time_endede':time_endede,'uis_g':uis_g,'info_g':info_g,'mms_no_auto':mms_no_auto,'date_today':date_today,'uis':uis,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")
def update_uis(request,uis):
    if request.session.get('employee_id') is not None:
        showRCD = requests.post(malasakit_api_showRCD).json()
        if showRCD['status'] == 'success':
            get_rcd  = showRCD['data']
        try:  
            now = datetime.now()
            time_started = datetime.strftime(now, '%I:%M:%S %p')
            request.session['start_time_upduis'] = time_started
            uis_details = UIS.objects.get(uis=uis)
            informant  = Informant.objects.get(uis=uis)
            iden_info = IdentifyingInformation.objects.get(uis=uis)
            loe= ListofExpenses.objects.get(uis=uis)
            conv_ls = loe.ligth_source.replace("[","").replace("]","").replace("'","")
            conv_ls_space = conv_ls.replace(" ","")
            new_ls = conv_ls_space.split(',')
            conv_ls_amt = loe.amt_ligth_source.replace("[","").replace("]","").replace("'","")
            conv_ls_space_amt = conv_ls_amt.replace(" ","")
            new_ls_amt = conv_ls_space_amt.split(',')
            conv_ws = loe.water_source.replace("[","").replace("]","").replace("'","")
            conv_ws_space = conv_ws.replace(" ","")
            new_ws  = conv_ws_space.split(',')
            conv_ws_amt = loe.amt_water_source.replace("[","").replace("]","").replace("'","")
            conv_ws_space_amt = conv_ws_amt.replace(" ","")
            new_ws_amt = conv_ws_space_amt.split(',')
            conv_other_expenses = loe.other_expenses.replace("[","").replace("]","").replace("'","")
            conv_other_expenses_space = conv_other_expenses.replace(" ","")
            new_oe = conv_other_expenses_space.split(',')

            conv_other_expenses_amt = loe.amt_other_expenses.replace("[","").replace("]","").replace("'","")
            conv_other_expenses_space_amt = conv_other_expenses_amt.replace(" ","")
            new_amt_oe = conv_other_expenses_space_amt.split(',')

            mm = ProblemPresented.objects.get(uis = uis)
            probpres_id = mm.problemPresented
            problem = mm.problem
            conv_problem = problem.replace("[","").replace("]","").replace("'","")
            f_problem = conv_problem.replace(" ","")
            fproblem = f_problem.split(',')
            prob_desc = mm.prob_desc
            conv_prob_desc = prob_desc.replace("[","").replace("]","").replace("'","")
            f_prob_desc = conv_prob_desc.split(',') 

            swa_desc = SWA.objects.get(uis = uis)

            famcom = FamilyComposition.objects.filter(uis = uis)
            mi_tot = 0
            for c in famcom:
                mi_tot += float(c.mi)
            num_famcom = FamilyComposition.objects.filter(uis = uis).count()
            famcom_osof = Fc_other_source.objects.filter(uis = uis)
            osof_amt_tot = 0
            for b in famcom_osof:
                if b.otherSources_of_fi_desc == 'CCT':
                    amt_osof = float(b.otherSources_of_fi)/2
                else:
                    amt_osof = float(b.otherSources_of_fi)
                osof_amt_tot += amt_osof
            # print(osof_amt_tot)

            reccom = Recommendations.objects.filter(uis = uis)
        except uis_details.DoesNotExist:
            raise Http404("Patient Doest not exist")
        return render(request, 'uis/update_uis.html',{'start_time':request.session['start_time_upduis'],'get_rcd':get_rcd,'probpres_id':probpres_id,'id_uis':uis,'osof_amt_tot':osof_amt_tot,'mi_tot':mi_tot,'num_famcom':num_famcom,'reccom':reccom,'famcom_osof':famcom_osof,'famcom':famcom,'swa_desc':swa_desc,'f_prob_desc':f_prob_desc,'fproblem':fproblem,'new_amt_oe':new_amt_oe,'new_oe':new_oe,'amt_ws':new_ws_amt,'ws':new_ws,'amt_ls':new_ls_amt,'ls':new_ls,'loe':loe,'iden_info':iden_info ,'uis_details':uis_details,'informant':informant,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")
# def update_famcom(request,uis):
#     if request.session.get('employee_id') is not None:
#         return render(request,'uis/update_famcom.html')
    
#     else:
#         return HttpResponseRedirect("/auth_login")
def process_update_uis(request,uis):
    if request.session.get('employee_id') is not None:
        now = datetime.now()
        try:
            if request.method == 'POST':
                date_today = datetime.strftime(now, '%Y-%m-%d')
                time_end = datetime.strftime(now,'%I:%M %p')
                time_today = request.session['start_time_upduis']

                #uis data
                tot_income = request.POST.get('tot_income')
                tot_expense = request.POST.get('tot_expense')
                
                category = request.POST.get('klass')
                num_famcom = int(request.POST.get('num_famcom',0))
                house_size = int(request.POST.get('housize', 0))
                f_hsize = house_size + num_famcom + 1
                phil_no = request.POST.get('phil_no')

                #informant data
                
                informant_upd = request.POST.get('informant_upd')
                noi = request.POST.get('noi').upper()
                rtp = request.POST.get('rtp').upper()
                cnums = request.POST.get('cnums')
                pa = request.POST.get('pa').upper()

                #identifying information
                iden_info_upd = request.POST.get('iden_info_upd')
                cn = request.POST.get('cn')
                sx = request.POST.get('gender')
                bdey = request.POST.get('bdate')
                age = request.POST.get('age')
                cs = request.POST.get('cs')
                rel = request.POST.get('rel')
                nat = request.POST.get('nat')
                hea = request.POST.get('hea')
                occu = request.POST.get('occu')
                mi = request.POST.get('mi')
                pt = request.POST.get('pt')
                pob = request.POST.get('pob')
                pea = request.POST.get('pea')
                pra = request.POST.get('pra')
                
                # #list of expenses
                listofExpenses_upd = request.POST.get('listofExpenses_upd')
                le_house = request.POST.get('le_house')
                le_amt_house = request.POST.get('le_amt_house')
                le_lot = request.POST.get('le_lot')
                le_amt_lot =request.POST.get('le_amt_lot')
                light_source = []
                water_source = []
                other_expenses = []
                desc_light_source = []
                desc_water_source = []
                desc_others_expenses = []
                prob_presented = []
                prob_presented_desc=[]
                elec = request.POST.get('elec', False)
                amt_elec_init = request.POST.get('amt_elec')
                kero = request.POST.get('kero', False)
                amt_kero_init = request.POST.get('amt_kero')
                cand = request.POST.get('cand', False)
                amt_cand_init = request.POST.get('amt_cand')
                oth = request.POST.get('oth', False)
                amt_oth_init = request.POST.get('amt_oth')
                if elec:
                    desc_elec = "ELECTRICITY"
                    amt_elec = float(amt_elec_init)
                else:
                    desc_elec = ""
                    amt_elec = 0
                    pass
                if kero:
                    desc_kero = "KEROSENE"
                    amt_kero = float(amt_kero_init)
                else:
                    desc_kero = ""
                    amt_kero = 0
                    pass
                if cand:
                    desc_cand = "CANDLE"
                    amt_cand = float(amt_cand_init)
                else:
                    desc_cand = ""
                    amt_cand = 0
                    pass
                if oth:
                    desc_oth = "OTHERS"
                    amt_oth = float(amt_oth_init)
                else:
                    desc_oth = ""
                    amt_oth = 0
                desc_light_source = [desc_elec,desc_kero,desc_cand,desc_oth]
                light_source= [amt_elec,amt_kero,amt_cand,amt_oth]
                water_source_public = request.POST.get('pub', False)
                amt_water_source_public_init = request.POST.get('amt_pub')
                water_source_nat = request.POST.get('natu', False)
                amt_water_source_nat_init = request.POST.get('amt_nat')
                water_source_wd = request.POST.get('wd', False)
                amt_water_source_wd_init = request.POST.get('amt_wd')
                water_source_min = request.POST.get('min', False)
                amt_water_source_min_init = request.POST.get('amt_min')
                if water_source_public:
                    desc_public = "PUBLIC"
                    amt_water_source_public = float(amt_water_source_public_init) 
                else:
                    desc_public = ""
                    amt_water_source_public = 0
                    pass
                if water_source_nat:
                    desc_natural = "NATURAL"
                    amt_water_source_nat = float(amt_water_source_nat_init)
                else:
                    desc_natural = ""
                    amt_water_source_nat = 0
                    pass
                if water_source_wd:
                    desc_wd = "WATER DISTRICT"
                    amt_water_source_wd =  float(amt_water_source_wd_init)
                else:
                    desc_wd = ""
                    amt_water_source_wd = 0
                    pass
                if water_source_min:
                    desc_min = "MINERAL"
                    amt_water_source_min = float(amt_water_source_min_init)
                else:
                    desc_min = ""
                    amt_water_source_min = 0
                desc_water_source=[desc_public,desc_natural,desc_wd,desc_min]
                water_source = [amt_water_source_public,amt_water_source_nat,amt_water_source_wd,amt_water_source_min]
                house = request.POST.get('house', False)
                amt_house_init = request.POST.get('amt_house')
                me = request.POST.get('me', False)
                amt_me_init = request.POST.get('amt_me')
                ip = request.POST.get('ip', False)
                amt_ip_init = request.POST.get('amt_ip')
                edu = request.POST.get('edu', False)
                amt_edu_init = request.POST.get('amt_edu')
                loan = request.POST.get('loan', False)
                amt_loan_init = request.POST.get('amt_loan')
                transpo = request.POST.get('transpo', False)
                amt_transpo_init = request.POST.get('amt_transpo')
                food = request.POST.get('food', False)
                amt_food_init = request.POST.get('amt_food')
                saving = request.POST.get('saving', False)
                amt_saving_init = request.POST.get('amt_saving')
                other = request.POST.get('other', False)
                amt_other_init = request.POST.get('amt_other')
                if house:
                    desc_house = "HOUSE"
                    amt_house = float(amt_house_init)
                else:
                    desc_house = ""
                    amt_house = 0
                    pass
                if me:
                    desc_me = "ME"
                    amt_me = float(amt_me_init)
                else:
                    desc_me = ""
                    amt_me = 0
                    pass
                if ip:
                    desc_ip = "IP"
                    amt_ip = float(amt_ip_init)
                else:
                    desc_ip = ""
                    amt_ip = 0
                    pass
                if edu:
                    desc_edu = "EDU"
                    amt_edu = float(amt_edu_init)
                else:
                    desc_edu = ""
                    amt_edu = 0
                    pass
                if loan:
                    desc_loan = "LOAN"
                    amt_loan = float(amt_loan_init)
                else:
                    desc_loan = ""
                    amt_loan = 0
                    pass
                if transpo:
                    desc_transpo = "TRANSPO"
                    amt_transpo = float(amt_transpo_init)
                else:
                    desc_transpo = ""
                    amt_transpo = 0
                    pass
                if food:
                    desc_food = "FOOD"
                    amt_food = float(amt_food_init)
                else:
                    desc_food=""
                    amt_food = 0
                    pass
                if saving:
                    desc_saving="SAVINGS"
                    amt_saving = float(amt_saving_init)
                else:
                    desc_saving=""
                    amt_saving = 0
                    pass
                if other:
                    desc_other = "OTHER"
                    amt_other = float(amt_other_init)
                else:
                    desc_other = ""
                    amt_other = 0
                desc_others_expenses = [desc_house,desc_me,desc_ip,desc_edu,desc_loan,desc_transpo,desc_food,desc_saving,desc_other]
                other_expenses = [amt_house,amt_me,amt_ip,amt_edu,amt_loan,amt_transpo,amt_food,amt_saving,amt_other]
            
                # # #problem Presented
                problemPresented_upd = request.POST.get('problemPresented_upd')
                hcop = request.POST.get('hcop', False)
                hcop_desc = request.POST.get('hcop_desc')
                fn = request.POST.get('fn', False)
                fn_desc = request.POST.get('fn_desc')
                emp = request.POST.get('emp', False)
                emp_desc = request.POST.get('emp_desc')
                ers = request.POST.get('ers', False)
                ers_desc = request.POST.get('ers_desc')
                hs = request.POST.get('hs', False)
                hs_desc = request.POST.get('hs_desc')
                osy = request.POST.get('osy', False)
                osy_desc = request.POST.get('osy_desc')
                if hcop:
                    n_hcop = "HCOP"
                    hcop_desc = hcop_desc
                else:
                    n_hcop = ''
                    hcop_desc=''
                if fn:
                    n_fn = "FN"
                    fn_desc = fn_desc
                else:
                    n_fn = ''
                    fn_desc=''
                if emp:
                    n_emp = "EMP"
                    emp_desc = emp_desc
                else:
                    n_emp = ''
                    emp_desc=''
                if ers:
                    n_ers = "ERS"
                    ers_desc = ers_desc
                else:
                    n_ers=''
                    ers_desc=''
                if hs:
                    n_hs = "HS"
                    hs_desc = hs_desc
                else:
                    n_hs = ''
                    hs_desc=''
                if osy:
                    n_osy = 'OSY'
                    osy_desc = osy_desc
                else:
                    n_osy = ''
                    osy_desc=''
                prob_presented = [n_hcop,n_fn,n_emp,n_ers,n_hs,n_osy]
                prob_presented_desc = [hcop_desc,fn_desc,emp_desc,ers_desc,hs_desc,osy_desc]
                
                #swa
                swa_upds = request.POST.get('swa_upd')
                desc_swa = request.POST.get('swa')

        except (KeyError, UIS.DoesNotExist):
            return render(request, 'uis/update_uis.html',{
                'error_message':"PROBLEM IN UPDATING",
                })
        else:
            uis_ups = UIS.objects.get(uis=uis)
            uis_ups.total_income = tot_income
            uis_ups.total_expense = tot_expense
            uis_ups.category = category
            uis_ups.householdsize = f_hsize
            uis_ups.phil_no = phil_no
            uis_ups.date= date_today
            uis_ups.save()

            upd_informant = Informant.objects.get(informant = informant_upd)
            upd_informant.fullname = noi
            upd_informant.relation_to_patient = rtp
            upd_informant.contact_number = cnums
            upd_informant.address = pa
            upd_informant.date_of_intake = date_today
            upd_informant.time_of_interview = time_today
            upd_informant.end_time_of_interview = time_end
            upd_informant.save()

            upd_iden_info = IdentifyingInformation.objects.get(identifyingInformation=iden_info_upd)
            upd_iden_info.client_name=cn
            upd_iden_info.gender=sx
            upd_iden_info.dob=bdey
            upd_iden_info.age=age
            upd_iden_info.cstat = cs
            upd_iden_info.religion = rel
            upd_iden_info.nationality = nat
            upd_iden_info.hea = hea
            upd_iden_info.occupation = occu
            upd_iden_info.mi = mi
            upd_iden_info.patient_type = pt
            upd_iden_info.pob = pob
            upd_iden_info.permanent_address = pea
            upd_iden_info.present_address = pra
            upd_iden_info.save()
            #family composition
            fam_com = request.POST.get('familycom')
            
            if fam_com:
                uis_id = UIS.objects.get(uis=uis)
                fam_data = json.loads(fam_com)
                for f in fam_data:
                    cname = f['cname']
                    fcgender = f['gender']
                    fccstat = f['cstat']
                    fcrtp = f['rtp']
                    fchea = f['hea']
                    fcoccu = f['occu']
                    fcmi = f['mi']
                    fcage = f['fage']
                    c = FamilyComposition(uis=uis_id,fullname = cname,gender=fcgender,cstat = fccstat,relation_to_patient = fcrtp,hea=fchea,occupation=fcoccu,mi=fcmi,age=fcage)
                    c.save()
                    fc_id = FamilyComposition.objects.get(familyComposition = c.familyComposition)
                    
            else:
                fc_id_init = request.POST.get('famicom_id')
                fc_id = FamilyComposition.objects.get(familyComposition = fc_id_init)
                fam_data = []
                
            fam_com_osof = request.POST.get('familycomosof')
            if fam_com_osof:
                uis_id = UIS.objects.get(uis=uis)
                famosof_data = json.loads(fam_com_osof)
                for y in famosof_data:
                    desc_osof = y['desc_osof']
                    amt_osof = y['amt_osof']
                    ex = Fc_other_source(uis=uis_id,familyComposition = fc_id,otherSources_of_fi_desc = desc_osof,otherSources_of_fi=amt_osof)
                    ex.save()
            else:
                famosof_data = []
            
            upd_listofExpenses = ListofExpenses.objects.get(listofExpenses = listofExpenses_upd)
            upd_listofExpenses.house = le_house
            upd_listofExpenses.amt_house = le_amt_house
            upd_listofExpenses.lot = le_lot
            upd_listofExpenses.amt_lot = le_amt_lot
            upd_listofExpenses.ligth_source = desc_light_source 
            upd_listofExpenses.amt_ligth_source = light_source
            upd_listofExpenses.water_source = desc_water_source
            upd_listofExpenses.amt_water_source = water_source
            upd_listofExpenses.other_expenses = desc_others_expenses
            upd_listofExpenses.amt_other_expenses = other_expenses
            upd_listofExpenses.save()

            upd_problemPresented = ProblemPresented.objects.get(problemPresented = problemPresented_upd)
            upd_problemPresented.problem = prob_presented
            upd_problemPresented.prob_desc = prob_presented_desc
            upd_problemPresented.save()

            upd_swa = SWA.objects.get(swa = swa_upds)
            upd_swa.swa_desc = desc_swa
            upd_swa.save()

            reccomendations = request.POST.get('reccomdata')
            if reccomendations:
                uis_id = UIS.objects.get(uis=uis)
                reccom_data = json.loads(reccomendations)
                for r in reccom_data:
                    mtoa = r['mtoa']
                    maos = r['maos']
                    mmoa = r['mmoa']
                    mfs = r['mfs']
                    gg = Recommendations(uis = uis_id,type_of_assistance = mtoa,amt_of_assistance = maos,mode_of_assistance = mmoa,fund_source = mfs)
                    gg.save()
            else:
                reccom_data = []
            redirect_url_with_args = f'/{uis}/update_uis'
            messages.success(request, "SUCCESSFULLY UPDATED")
            return redirect(redirect_url_with_args)  
    else:
        return HttpResponseRedirect("/auth_login")
def del_famcom(request, uis_id,famcom_id):
    try:
        FamilyComposition.objects.filter(familyComposition=famcom_id).delete()
        messages.success(request, 'Sucessfully Deleted!')
    except RestrictedError:
        messages.warning(request, 'Cannot Delete this Data!')
    redirect_url_with_args = f'/{uis_id}/update_uis'
    return redirect(redirect_url_with_args)

def del_reccom(request, uis_id,reccom_id):
    try:
        Recommendations.objects.filter(recommendation=reccom_id).delete()
        messages.success(request, 'Sucessfully Deleted!')
    except RestrictedError:
        messages.warning(request, 'Cannot Delete this Data!')
    redirect_url_with_args = f'/{uis_id}/update_uis'
    return redirect(redirect_url_with_args)

def del_famcom_osof(request, uis_id,osof_id):
    try:
        Fc_other_source.objects.filter(fc_other_source=osof_id).delete()
        messages.success(request, 'Sucessfully Deleted!')
    except RestrictedError:
        messages.warning(request, 'Cannot Delete this Data!')
    redirect_url_with_args = f'/{uis_id}/update_uis'
    return redirect(redirect_url_with_args)

def update_msstool(request,mssat):
    if request.session.get('employee_id') is not None:
        try:
            now = datetime.now()
            date_today = datetime.strftime(now, '%Y-%m-%d')
            time_starts = datetime.strftime(now, '%I:%M %p')
            request.session['mssat_start']= time_starts
            time_endede = datetime.strftime(now, '%I:%M %p')
            mssat_details = MSSAT.objects.get(mssat=mssat)
            conv_fs = mssat_details.fuel_source.replace("[","").replace("]","").replace("'","")
            conv_fs_space = conv_fs.replace(" ","")
            new_fs = conv_fs_space.split(',')
            conv_fs_amt = mssat_details.amt_fuel_source.replace("[","").replace("]","").replace("'","")
            conv_fs_space_amt = conv_fs_amt.replace(" ","")
            new_fs_amt = conv_fs_space_amt.split(',')

            uis_g = UIS.objects.get(uis=mssat_details.uis_id)
            info_g = Informant.objects.get(uis=mssat_details.uis_id)
        except mssat_details.DoesNotExist:
            raise Http404("Patient Doest not exist")
        return render(request, 'uis/upd_msstool.html',{'uis_g':uis_g,'info_g':info_g,'time_start':request.session['mssat_start'],'time_endede':time_endede,'date_today':date_today,'fs':new_fs,'amt_fs':new_fs_amt,'mssat_details':mssat_details,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")


def process_update_mssat(request, mssat):
    if request.session.get('employee_id') is not None:
        now = datetime.now()
        date_today = datetime.strftime(now, '%Y-%m-%d')
        try:
            if request.method == 'POST':
                fuel_src = []
                amt_fuel_src = []
                doac = request.POST.get('doac')
                basic_ward = request.POST.get('basic_ward')
                venue = request.POST.get('venue')
                catss = request.POST.get('categorys')
                mss_no = request.POST.get('mss_no')
                src_referal_name = request.POST.get('src_referal_name')
                cnum = request.POST.get('cnum')
                address = request.POST.get('address')
                tla = request.POST.get('tla')
                phil_mem = request.POST.get('phil_mem')
                marginalized_sec_mem = request.POST.get('marginalized_sec_mem')
                clothing_amt = request.POST.get('clothing_amt')
                duration_of_prob = request.POST.get('duration_of_prob')
                prev_treatment = request.POST.get('prev_treatment')
                health_accessibility_prob = request.POST.get('health_accessibility_prob')
                lpg = request.POST.get('lpg', False)
                amt_lpg = request.POST.get('amt_lpg')
                elec = request.POST.get('elec', False)
                amt_elec = request.POST.get('amt_elec')
                char = request.POST.get('char', False)
                amt_char = request.POST.get('amt_char')
                fwood = request.POST.get('fwood', False)
                amt_fwood = request.POST.get('amt_fwood')
        
                if lpg:
                    f_lpg = "LPG"
                    f_amt_lpg =float(amt_lpg)
                else:
                    f_lpg = ""
                    f_amt_lpg = 0
                    pass
                # if elec:
                #     f_elec = "ELECTRICITY"
                #     f_amt_elec =float(amt_elec)
                # else:
                #     f_elec = ""
                #     f_amt_elec = 0
                #     pass
                if char:
                    f_char = "CHARCOAL"
                    f_amt_char =float(amt_char)
                else:
                    f_char = ""
                    f_amt_char = 0
                    pass
                if fwood:
                    f_fwood = "FIREWOOD"
                    f_amt_fwood =float(amt_fwood)
                else:
                    f_fwood = ""
                    f_amt_fwood = 0
                fuel_src = [f_lpg,f_char,f_fwood]
                amt_fuel_src = [f_amt_lpg,f_amt_char,f_amt_fwood]
        except (KeyError, MSSAT.DoesNotExist):
            return render(request, 'uis/upd_msstool.html',{
                'error_message':"PROBLEM IN UPDATING",
                })
        else:
            mssat_id = MSSAT.objects.get(mssat = mssat)
            mssat_id.doac = doac
            mssat_id.basic_ward = basic_ward
            mssat_id.venue = venue
            mssat_id.category = catss
            mssat_id.mss_no = mss_no
            mssat_id.src_referal_name = src_referal_name
            mssat_id.cnum = cnum
            mssat_id.address = address
            mssat_id.tla = tla
            mssat_id.phil_mem = phil_mem
            mssat_id.marginalized_sec_mem = marginalized_sec_mem
            mssat_id.clothing_amt = clothing_amt
            mssat_id.duration_of_prob = duration_of_prob
            mssat_id.prev_treatment = prev_treatment
            mssat_id.health_accessibility_prob = health_accessibility_prob
            mssat_id.fuel_source = fuel_src
            mssat_id.amt_fuel_source = amt_fuel_src
            mssat_id.save()
            redirect_url_with_args = f'/{mssat}/update_msstool'
            return redirect(redirect_url_with_args)
    else:
        return HttpResponseRedirect("/auth_login")

def uis_excel(request):
    if request.session.get('employee_id') is not None:
        uis_excel = UIS_copy.objects.all()
        if request.method == 'POST':
            now = datetime.now()
            time_started = datetime.strftime(now, '%I:%M:%S %p')
            request.session['start_time_uietoexcel'] = time_started
            uis_file = request.FILES.get('fileinput')
            us = UIS_copy(uis_excel = uis_file)
            us.save()
        return render(request, 'uis/import_uis_excel.html',{'uis_excel':uis_excel,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")

def exceltoweb_uis(request,named):
    if request.session.get('employee_id') is not None:
        showRCD = requests.post(malasakit_api_showRCD).json()
        get_uisexcel_name = UIS_copy.objects.filter(uis_copy =named)
        name_patien  =""
        for g in get_uisexcel_name:
            name_patient = g.uis_excel
        if showRCD['status'] == 'success':
            get_rcd  = showRCD['data']
        # patientname = name.replace("_"," ")
        # print(patientname)
        now = datetime.now()
        date_today = datetime.strftime(now, '%Y-%m-%d')
        date_show = datetime.strftime(now, '%b %d, %Y')
        time_show = request.session['start_time_uietoexcel']
        
        wb = load_workbook(f'media/{name_patient}')
        w = wb.active 
        # informant details
        philhealt_no = w["D3"].value
        hospo_no = w["Q3"].value
        noi = w["G6"].value
        id_rtp = w["Q6"].value
        inaddress_init = w["D7"].value
        if inaddress_init =='=E14':
            inaddress = w["E14"].value
        elif inaddress_init == '=E16':
            inaddress = w["E16"].value
        else:
            inaddress = inaddress_init
        incnum = w["Q7"].value
        #identifying information
        iicname_init = w["D10"].value
        if iicname_init == '=G6':
            iicname = w["G6"].value
        else:
            iicname = iicname_init
        iisex = w["R10"].value
        iidob = w["A12"].value
        iipob = w["M12"].value
        iipa_init = w["E14"].value
        if iipa_init =='=D7':
            iipa = w["D7"].value
        elif iipa_init == '=E16':
            iipa = w["E16"].value
        else:
            iipa = iipa_init
        iipra_init = w["E16"].value
        if iipra_init == '=D7':
            iipra = w["D7"].value
        elif iipra_init == '=E14':
            iipra = w["E14"].value
            if iipra == '=D7':
                iipra = w["D7"].value
        else:
            iipra = iipra_init
        iinat = w["N19"].value
        iirel = w["D19"].value
        iioccu = w["D24"].value
        iimi_init = w["P24"].value

        swa = w["A74"].value
        if iimi_init is None:
            iimi = 0
        else:
            iimi = iimi_init
        def calculate_aged(birth_date):
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        age = calculate_aged(iidob)
        
        # kita = w["R31"].value
        # rkita = kita.replace('=','')
        # result=eval(rkita)
        start_row = 31
        end_row = 42
        name = 'A'
        sex = 'I'
        cstat = 'K'
        rtp = 'L'
        hea = 'M'
        occu = 'P'
        mi = 'R'
        datas = []

        for row in range(start_row, end_row + 1):
            name_value = w[f'{name}{row}'].value
            sex_value = w[f'{sex}{row}'].value
            cstat_value = w[f'{cstat}{row}'].value
            rtp_value = w[f'{rtp}{row}'].value
            hea_value = w[f'{hea}{row}'].value
            occu_value = w[f'{occu}{row}'].value
            init_mi = w[f'{mi}{row}'].value
            if init_mi is not None:
                mi_value = init_mi
                str_mivalue = str(init_mi)
                if str_mivalue[:1] == '=':
                    mi_f = init_mi.replace('=','')
                    mi_value = eval(mi_f)
            elif init_mi == '':
                mi_value = 0
            else:
                mi_value = 0
            if name_value is not None:
                datas.append({
                    'cname':name_value,
                    'gender':sex_value,
                    'cstat':cstat_value,
                    'rtp':rtp_value,
                    'hea':hea_value,
                    'occu':occu_value,
                    'mi':mi_value
                })
            
            else:
                break
        
        house_amt_owned = w["D50"].value
        house_amt_rented = w["D51"].value
        house_amt_shared = w["D52"].value
        house_amt_others = w["D53"].value
        if house_amt_owned is not None:
            house_desc = 'OWNED'
            house_amt = house_amt_owned
        elif house_amt_rented is not None:
            house_desc = 'RENTED'
            house_amt = house_amt_rented
        elif house_amt_shared is not None:
            house_desc = 'SHARED'
            house_amt = house_amt_shared
        elif house_amt_others is not None:
            house_desc = 'OTHERS'
            house_amt = house_amt_others
        else:
            house_desc = 'OWNED'
            house_amt = 0

        lot_amt_owned = w["D56"].value
        lot_amt_shared = w["D57"].value
        lot_amt_government = w["D58"].value
        lot_amt_private_property = w["D59"].value
        if lot_amt_owned is not None:
            lot_desc = 'OWNED'
            lot_amt = lot_amt_owned
        elif lot_amt_shared is not None:
            lot_desc = 'SHARED'
            lot_amt = lot_amt_shared
        elif lot_amt_government is not None:
            lot_desc = 'GOVERNMENT'
            lot_amt = lot_amt_government
        elif lot_amt_private_property is not None:
            lot_desc = 'PRIVATE PROPERTY'
            lot_amt = lot_amt_private_property
        else:
            lot_desc = 'OWNED'
            lot_amt = 0

        liwanag_amt_elec = w["K50"].value
        liwanag_amt_kero = w["K51"].value
        liwanag_amt_candle = w["K52"].value
        liwanag_amt_others = w["K53"].value

        tubig_amt_public = w["I56"].value
        tubig_amt_nat_init = w["I57"].value
        if tubig_amt_nat_init == 'ARTESAN':
            tubig_amt_nat = 0
        else:
            tubig_amt_nat = tubig_amt_nat_init

        tubig_amt_wd = w["I58"].value
        tubig_amt_wilkins = w["I59"].value

        excel_househelp_init = w["Q50"].value
        if excel_househelp_init is not None:
            excel_househelp = excel_househelp_init
            str_excel_househelp = str(excel_househelp_init)
            if str_excel_househelp[:1] == '=':
                excel_househelp_f = excel_househelp_init.replace('=','')
                excel_househelp = eval(excel_househelp_f)
        elif excel_househelp_init == '':
            excel_househelp = None
        else:
            excel_househelp = None
        excel_educ_init = w["Q51"].value
        if excel_educ_init is not None:
            excel_educ = excel_educ_init
            str_excel_educ = str(excel_educ_init)
            if str_excel_educ[:1] == '=':
                excel_educ_f = excel_educ_init.replace('=','')
                excel_educ = eval(excel_educ_f)
        elif excel_educ_init == '':
            excel_educ = None
        else:
            excel_educ = None
        excel_food_init = w["Q52"].value
        if excel_food_init is not None:
            excel_food = excel_food_init
            str_excel_food = str(excel_food_init)
            if str_excel_food[:1] == '=':
                excel_food_f = excel_food_init.replace('=','')
                excel_food = eval(excel_food_f)
        elif excel_food_init == '':
            excel_food = None
        else:
            excel_food = None
        excel_medxp_init = w["Q53"].value
        if excel_medxp_init is not None:
            excel_medxp = excel_medxp_init
            str_excel_medxp = str(excel_medxp_init)
            if str_excel_medxp[:1] == '=':
                excel_medxp_f = excel_medxp_init.replace('=','')
                excel_medxp = eval(excel_medxp_f)
        elif excel_medxp_init == '':
            excel_medxp = None
        else:
            excel_medxp = None
        excel_loan_init = w["Q54"].value
        if excel_loan_init is not None:
            excel_loan = excel_loan_init
            str_excel_loan = str(excel_loan_init)
            if str_excel_loan[:1] == '=':
                excel_loan_f = excel_loan_init.replace('=','')
                excel_loan = eval(excel_loan_f)
        elif excel_loan_init == '':
            excel_loan = None
        else:
            excel_loan = None
        excel_savings_init = w["Q55"].value
        if excel_savings_init is not None:
            excel_savings = excel_savings_init
            str_excel_savings = str(excel_savings_init)
            if str_excel_savings[:1] == '=':
                excel_savings_f = excel_savings_init.replace('=','')
                excel_savings = eval(excel_savings_f)
        elif excel_savings_init == '':
            excel_savings = None
        else:
            excel_savings = None
        excel_inpr_init = w["Q56"].value
        if excel_inpr_init is not None:
            excel_inpr = excel_inpr_init
            str_excel_inpr = str(excel_inpr_init)
            if str_excel_inpr[:1] == '=':
                excel_inpr_f = excel_inpr_init.replace('=','')
                excel_inpr = eval(excel_inpr_f)
        elif excel_inpr_init == '':
            excel_inpr = None
        else:
            excel_inpr = None
        excel_trans_init = w["Q57"].value
        if excel_trans_init is not None:
            excel_trans = excel_trans_init
            str_excel_trans = str(excel_trans_init)
            if str_excel_trans[:1] == '=':
                excel_trans_f = excel_trans_init.replace('=','')
                excel_trans = eval(excel_trans_f)
        elif excel_trans_init == '':
            excel_trans = None
        else:
            excel_trans = None
        excel_oth_init = w["Q58"].value
        if excel_oth_init is not None:
            excel_oth = excel_oth_init
            str_excel_oth = str(excel_oth_init)
            if str_excel_oth[:1] == '=':
                excel_oth_f = excel_oth_init.replace('=','')
                excel_oth = eval(excel_oth_f)
        elif excel_oth_init == '':
            excel_oth = None
        else:
            excel_oth = None

        excel_hcop_init = w["F63"].value
        if excel_hcop_init is None:
            excel_hcop = w["F62"].value
        else:
            excel_hcop = w["F63"].value
        excel_fn = w["F64"].value
        excel_emp = w["F65"].value
        excel_ecosrc = w["N63"].value
        excel_hawsing = w["N64"].value
        excel_ader = w["N65"].value

        fam_osof = w["A44"].value
        fam_osof1 = w["A45"].value
        fam_osof2 = w["A46"].value

        amt_fam_osof = w["I44"].value
        amt_fam_osof1 = w["I45"].value
        amt_fam_osof2 = w["I46"].value

        return render(request, 'uis/excel_to_web_uis.html',{'amt_fam_osof':amt_fam_osof,'amt_fam_osof1':amt_fam_osof1,'amt_fam_osof2':amt_fam_osof2,'fam_osof':fam_osof,'fam_osof1':fam_osof1,'fam_osof2':fam_osof2,'excel_ader':excel_ader,'excel_hawsing':excel_hawsing,'excel_ecosrc':excel_ecosrc,'excel_emp':excel_emp,'excel_fn':excel_fn,'excel_hcop':excel_hcop,'excel_oth':excel_oth,'excel_trans':excel_trans,'excel_inpr':excel_inpr,'excel_savings':excel_savings,'excel_loan':excel_loan,'excel_medxp':excel_medxp,'excel_food':excel_food,'excel_educ':excel_educ,'excel_househelp':excel_househelp,'tubig_amt_public':tubig_amt_public,'tubig_amt_nat':tubig_amt_nat,'tubig_amt_wd':tubig_amt_wd,'tubig_amt_wilkins':tubig_amt_wilkins,'liwanag_amt_others':liwanag_amt_others,'liwanag_amt_candle':liwanag_amt_candle,'liwanag_amt_kero':liwanag_amt_kero,'liwanag_amt_elec':liwanag_amt_elec,'lot_amt':lot_amt,'house_amt':house_amt,'lot_desc':lot_desc,'house_desc':house_desc,'get_rcd':get_rcd,'swa':swa,'fc_datas':datas,'iimi':iimi,'iinat':iinat,'iirel':iirel,'iioccu':iioccu,'iipa':iipa,'iipra':iipra,'iiage':age,'iipob':iipob,'iidob':iidob,'iisex':iisex,'iicname':iicname,'incnum':incnum,'inaddress':inaddress,'id_rtp':id_rtp,'noi':noi,'time_show':time_show,'date_show':date_show,'hospo_no':hospo_no,'philhealt_no':philhealt_no,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")
def add_uis_excel(request):
    if request.session.get('employee_id') is not None:
        now = datetime.now()
        complain = ""
        if request.method == 'POST':
            date_today = datetime.strftime(now, '%Y-%m-%d')
            time_end = datetime.strftime(now,'%I:%M %p')
            time_today =  request.session['start_time_uietoexcel']
            
            #informant data
            noi = request.POST.get('noi').upper()
            rtp = request.POST.get('rtp').upper()
            cnums = request.POST.get('cnums')
            pa = request.POST.get('pa').upper()
            tot_income = request.POST.get('tot_income')
            tot_expense = request.POST.get('tot_expense')
            category = request.POST.get('klass')
            house_size = request.POST.get('housize')
            f_hsize = int(house_size) + 1
            phil_no = request.POST.get('phil_no')
            hospno = request.POST.get('hosp_no_excel')
            uis_add = UIS(date = date_today,hospno = hospno,phil_no=phil_no,total_income = tot_income,total_expense = tot_expense,category=category,householdsize = f_hsize)
            uis_add.save()
            if uis_add.uis:
                uis_id = UIS.objects.get(uis = uis_add.uis)
                # informant
                a = Informant(uis=uis_id,date_of_intake = date_today,time_of_interview=time_today,end_time_of_interview=time_end,fullname=noi,relation_to_patient = rtp,contact_number = cnums,address = pa)
                a.save()
                    
                #identifying information
                cn = request.POST.get('cn')
                sx = request.POST.get('gender')
                bdey = request.POST.get('bdate')
                age = request.POST.get('age')
                cs = request.POST.get('cs')
                rel = request.POST.get('rel')
                nat = request.POST.get('nat')
                hea = request.POST.get('hea')
                occu = request.POST.get('occu')
                mi = request.POST.get('mi')
                pt = request.POST.get('pt')
                pob = request.POST.get('pob')
                pea = request.POST.get('pea')
                pra = request.POST.get('pra')
                b = IdentifyingInformation(uis=uis_id,client_name = cn,gender=sx,dob = bdey,age=age,cstat = cs,religion = rel,nationality = nat,hea=hea,occupation = occu,mi=mi,patient_type=pt,pob=pob,permanent_address=pea,present_address=pra)
                b.save()

                #family composition
                fam_com = request.POST.get('familycom')
                  
                if fam_com:
                    fam_data = json.loads(fam_com)
                    for f in fam_data:
                        cname = f['cname']
                        fcgender = f['gender']
                        fccstat = f['cstat']
                        fcrtp = f['rtp']
                        fchea = f['hea']
                        fcoccu = f['occu']
                        fcmi = f['mi']
                        fcage = f['fage']
                        c = FamilyComposition(uis=uis_id,fullname = cname,gender=fcgender,cstat = fccstat,relation_to_patient = fcrtp,hea=fchea,occupation=fcoccu,mi=fcmi,age=fcage)
                        c.save()
                        fc_id = FamilyComposition.objects.get(familyComposition = c.familyComposition)
                elif fam_com == '' or fam_com is None:
                    c = FamilyComposition(uis=uis_id,fullname = cn,gender=sx,cstat = cs,relation_to_patient = "SELF", hea=hea,occupation=occu,mi=mi,age=age)
                    c.save()
                    fc_id = FamilyComposition.objects.get(familyComposition = c.familyComposition)
                else:
                    fam_data = []
                fam_com_osof = request.POST.get('familycomosof')
                if fam_com_osof:
                    famosof_data = json.loads(fam_com_osof)
                    for y in famosof_data:
                        desc_osof = y['desc_osof']
                        amt_osof = y['amt_osof']
                        x = Fc_other_source(uis=uis_id,familyComposition = fc_id,otherSources_of_fi_desc = desc_osof,otherSources_of_fi=amt_osof)
                        x.save()
                else:
                    famosof_data = []

                # #list of expenses
                le_house = request.POST.get('le_house')
                le_amt_house = request.POST.get('le_amt_house')
                le_lot = request.POST.get('le_lot')
                le_amt_lot =request.POST.get('le_amt_lot')
                light_source = []
                water_source = []
                other_expenses = []
                desc_light_source = []
                desc_water_source = []
                desc_others_expenses = []
                prob_presented = []
                prob_presented_desc=[]

                elec = request.POST.get('elec', False)
                amt_elec_init = request.POST.get('amt_elec')
                kero = request.POST.get('kero', False)
                amt_kero_init = request.POST.get('amt_kero')
                cand = request.POST.get('cand', False)
                amt_cand_init = request.POST.get('amt_cand')
                oth = request.POST.get('oth', False)
                amt_oth_init = request.POST.get('amt_oth')
                if elec:
                    desc_elec = "ELECTRICITY"
                    amt_elec = float(amt_elec_init)
                else:
                    desc_elec = ""
                    amt_elec = 0
                    pass
                if kero:
                    desc_kero = "KEROSENE"
                    amt_kero = float(amt_kero_init)
                else:
                    desc_kero = ""
                    amt_kero = 0
                    pass
                if cand:
                    desc_cand = "CANDLE"
                    amt_cand = float(amt_cand_init)
                else:
                    desc_cand = ""
                    amt_cand = 0
                    pass
                if oth:
                    desc_oth = "OTHERS"
                    amt_oth = float(amt_oth_init)
                else:
                    desc_oth = ""
                    amt_oth = 0
                desc_light_source = [desc_elec,desc_kero,desc_cand,desc_oth]
                light_source= [amt_elec,amt_kero,amt_cand,amt_oth]
                        
                water_source_public = request.POST.get('pub', False)
                amt_water_source_public_init = request.POST.get('amt_pub')
                water_source_nat = request.POST.get('natu', False)
                amt_water_source_nat_init = request.POST.get('amt_nat')
                water_source_wd = request.POST.get('wd', False)
                amt_water_source_wd_init = request.POST.get('amt_wd')
                water_source_min = request.POST.get('min', False)
                amt_water_source_min_init = request.POST.get('amt_min')
                if water_source_public:
                    desc_public = "PUBLIC"
                    amt_water_source_public = float(amt_water_source_public_init) 
                else:
                    desc_public = ""
                    amt_water_source_public = 0
                    pass
                if water_source_nat:
                    desc_natural = "NATURAL"
                    amt_water_source_nat = float(amt_water_source_nat_init)
                else:
                    desc_natural = ""
                    amt_water_source_nat = 0
                    pass
                if water_source_wd:
                    desc_wd = "WATER DISTRICT"
                    amt_water_source_wd =  float(amt_water_source_wd_init)
                else:
                    desc_wd = ""
                    amt_water_source_wd = 0
                    pass
                if water_source_min:
                    desc_min = "MINERAL"
                    amt_water_source_min = float(amt_water_source_min_init)
                else:
                    desc_min = ""
                    amt_water_source_min = 0
                desc_water_source=[desc_public,desc_natural,desc_wd,desc_min]
                water_source = [amt_water_source_public,amt_water_source_nat,amt_water_source_wd,amt_water_source_min]
                        
                house = request.POST.get('house', False)
                amt_house_init = request.POST.get('amt_house')
                me = request.POST.get('me', False)
                amt_me_init = request.POST.get('amt_me')
                ip = request.POST.get('ip', False)
                amt_ip_init = request.POST.get('amt_ip')
                edu = request.POST.get('edu', False)
                amt_edu_init = request.POST.get('amt_edu')
                loan = request.POST.get('loan', False)
                amt_loan_init = request.POST.get('amt_loan')
                transpo = request.POST.get('transpo', False)
                amt_transpo_init = request.POST.get('amt_transpo')
                food = request.POST.get('food', False)
                amt_food_init = request.POST.get('amt_food')
                saving = request.POST.get('saving', False)
                amt_saving_init = request.POST.get('amt_saving')
                other = request.POST.get('other', False)
                amt_other_init = request.POST.get('amt_other')
                if house:
                    desc_house = "HOUSE"
                    amt_house = float(amt_house_init)
                else:
                    desc_house = ""
                    amt_house = 0
                    pass
                if me:
                    desc_me = "ME"
                    amt_me = float(amt_me_init)
                else:
                    desc_me = ""
                    amt_me = 0
                    pass
                if ip:
                    desc_ip = "IP"
                    amt_ip = float(amt_ip_init)
                else:
                    desc_ip = ""
                    amt_ip = 0
                    pass
                if edu:
                    desc_edu = "EDU"
                    amt_edu = float(amt_edu_init)
                else:
                    desc_edu = ""
                    amt_edu = 0
                    pass
                if loan:
                    desc_loan = "LOAN"
                    amt_loan = float(amt_loan_init)
                else:
                    desc_loan = ""
                    amt_loan = 0
                    pass
                if transpo:
                    desc_transpo = "TRANSPO"
                    amt_transpo = float(amt_transpo_init)
                else:
                    desc_transpo = ""
                    amt_transpo = 0
                    pass
                if food:
                    desc_food = "FOOD"
                    amt_food = float(amt_food_init)
                else:
                    desc_food=""
                    amt_food = 0
                    pass
                if saving:
                    desc_saving="SAVINGS"
                    amt_saving = float(amt_saving_init)
                else:
                    desc_saving=""
                    amt_saving = 0
                    pass
                if other:
                    desc_other = "OTHER"
                    amt_other = float(amt_other_init)
                else:
                    desc_other = ""
                    amt_other = 0
                desc_others_expenses = [desc_house,desc_me,desc_ip,desc_edu,desc_loan,desc_transpo,desc_food,desc_saving,desc_other]
                other_expenses = [amt_house,amt_me,amt_ip,amt_edu,amt_loan,amt_transpo,amt_food,amt_saving,amt_other]
                d = ListofExpenses(uis = uis_id, house = le_house,amt_house = le_amt_house,lot=le_lot,amt_lot=le_amt_lot,ligth_source=desc_light_source,amt_ligth_source = light_source,water_source=desc_water_source,amt_water_source = water_source,other_expenses=desc_others_expenses,amt_other_expenses = other_expenses)
                d.save()

                # # #problem Presented

                hcop = request.POST.get('hcop', False)
                hcop_desc = request.POST.get('hcop_desc')
                fn = request.POST.get('fn', False)
                fn_desc = request.POST.get('fn_desc')
                emp = request.POST.get('emp', False)
                emp_desc = request.POST.get('emp_desc')
                ers = request.POST.get('ers', False)
                ers_desc = request.POST.get('ers_desc')
                hs = request.POST.get('hs', False)
                hs_desc = request.POST.get('hs_desc')
                osy = request.POST.get('osy', False)
                osy_desc = request.POST.get('osy_desc')
                if hcop:
                    n_hcop = "HCOP"
                    hcop_desc = hcop_desc
                else:
                    n_hcop = ''
                    hcop_desc=''

                if fn:
                    n_fn = "FN"
                    fn_desc = fn_desc
                else:
                    n_fn = ''
                    fn_desc=''
                if emp:
                    n_emp = "EMP"
                    emp_desc = emp_desc
                else:
                    n_emp = ''
                    emp_desc=''
                if ers:
                    n_ers = "ERS"
                    ers_desc = ers_desc
                else:
                    n_ers=''
                    ers_desc=''
                if hs:
                    n_hs = "HS"
                    hs_desc = hs_desc
                else:
                    n_hs = ''
                    hs_desc=''
                if osy:
                    n_osy = 'OSY'
                    osy_desc = osy_desc
                else:
                    n_osy = ''
                    osy_desc=''
                prob_presented = [n_hcop,n_fn,n_emp,n_ers,n_hs,n_osy]
                prob_presented_desc = [hcop_desc,fn_desc,emp_desc,ers_desc,hs_desc,osy_desc]
                e = ProblemPresented(uis = uis_id,problem= prob_presented,prob_desc = prob_presented_desc)
                e.save()

                #swa
                swa = request.POST.get('swa')
                f = SWA(uis = uis_id,swa_desc = swa)
                f.save()

                # reccomendations
                reccomendations = request.POST.get('reccomdata')
                if reccomendations:
                    reccom_data = json.loads(reccomendations)
                    for r in reccom_data:
                        mtoa = r['mtoa']
                        maos = r['maos']
                        mmoa = r['mmoa']
                        mfs = r['mfs']
                        g = Recommendations(uis = uis_id,type_of_assistance = mtoa,amt_of_assistance = maos,mode_of_assistance = mmoa,fund_source = mfs)
                        g.save()
                else:
                    reccom_data = []
                mssatcheck = request.POST.get('mssatcheck',False)
                if mssatcheck:
                    fuel_src = []
                    amt_fuel_src = []
                    doac = request.POST.get('doac')
                    basic_ward = request.POST.get('basic_ward')
                    non_basic = request.POST.get('non_basic')
                    mss_no = request.POST.get('mss_no')
                    src_referal_name = request.POST.get('src_referal_name')
                    cnum = request.POST.get('cnum')
                    address = request.POST.get('address')
                    employer = request.POST.get('employer')
                    tla = request.POST.get('tla')
                    phil_mem = request.POST.get('phil_mem')
                    mswd_cassif = request.POST.get('mswd_cassif')
                    marginalized_sec_mem = request.POST.get('marginalized_sec_mem')
                    clothing_amt = request.POST.get('clothing_amt')
                    duration_of_prob = request.POST.get('duration_of_prob')
                    prev_treatment = request.POST.get('prev_treatment')
                    health_accessibility_prob = request.POST.get('health_accessibility_prob')
                    lpg = request.POST.get('lpg', False)
                    amt_lpg = request.POST.get('amt_lpg')
                    elec = request.POST.get('elec', False)
                    amt_elec = request.POST.get('m_amt_elec')
                    char = request.POST.get('char', False)
                    amt_char = request.POST.get('amt_char')
                    fwood = request.POST.get('fwood', False)
                    amt_fwood = request.POST.get('amt_fwood')
                    if lpg:
                        f_lpg = "LPG"
                        f_amt_lpg =float(amt_lpg)
                    else:
                        f_lpg = ""
                        f_amt_lpg = 0
                        pass
                    if elec:
                        f_elec = "ELECTRICITY"
                        f_amt_elec =float(amt_elec)
                    else:
                        f_elec = ""
                        f_amt_elec = 0
                        pass
                    if char:
                        f_char = "CHARCOAL"
                        f_amt_char =float(amt_char)
                    else:
                        f_char = ""
                        f_amt_char = 0
                        pass
                    if fwood:
                        f_fwood = "FIREWOOD"
                        f_amt_fwood =float(amt_fwood)
                    else:
                        f_fwood = ""
                        f_amt_fwood = 0
                    fuel_src = [f_lpg,f_elec,f_char,f_fwood]
                    amt_fuel_src = [f_amt_lpg,f_amt_elec,f_amt_char,f_amt_fwood]
                    aa = MSSAT(uis=uis_id,doac = doac,basic_ward=basic_ward,non_basic = non_basic,mss_no=mss_no,tla=tla,src_referal_name=src_referal_name,address=address,cnum=cnum,employer=employer,phil_mem=phil_mem,mswd_cassif=mswd_cassif,marginalized_sec_mem=marginalized_sec_mem,fuel_source = fuel_src,amt_fuel_source = amt_fuel_src,clothing_amt=clothing_amt,duration_of_prob=duration_of_prob,prev_treatment=prev_treatment,health_accessibility_prob=health_accessibility_prob)
                    aa.save()
                else:
                    mssatcheck = []
                    pass
                    
                if mssatcheck:
                        
                    upd_has_mssat = UIS.objects.get(uis = uis_add.uis)
                    upd_has_mssat.has_mssat = True
                    upd_has_mssat.save()
                    redirect_url_with_args = f'/{uis_id}/mssat_pdf'
                else:
                    redirect_url_with_args = f'/{uis_id}/uis_pdf'
                messages.success(request, "SUCCESSFULLY ADDED")
                return redirect(redirect_url_with_args)
        return HttpResponseRedirect("/uis_list")
    else:
        return HttpResponseRedirect("/auth_login")
def walkin_page(request):
    if request.session.get('employee_id') is not None:
        now = datetime.now()
        date_show = datetime.strftime(now, '%b %d, %Y')
        time_show = datetime.strftime(now, '%I:%M %p')
        time_started = datetime.strftime(now, '%I:%M:%S %p')
        request.session['start_time_walkin'] = time_started
        showRCD = requests.post(malasakit_api_showRCD).json()

        if showRCD['status'] == 'success':
            get_rcd  = showRCD['data']
        return render(request, 'uis/walkin_uis.html',{'get_rcd':get_rcd,'time_show':request.session['start_time_walkin'],'date_show':date_show,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")
def walkin_uis(request):
    if request.session.get('employee_id') is not None:
        now = datetime.now()
        
        complain = ""
        if request.method == 'POST':
            date_today = datetime.strftime(now, '%Y-%m-%d')
            time_end = datetime.strftime(now,'%I:%M %p')
            time_today = request.session['start_time_walkin']
            
            #informant data
            noi = request.POST.get('noi').upper()
            rtp = request.POST.get('rtp').upper()
            cnums = request.POST.get('cnums')
            pa = request.POST.get('pa').upper()
            tot_income = request.POST.get('tot_income')
            tot_expense = request.POST.get('tot_expense')
            category = request.POST.get('klass')
            house_size = request.POST.get('housize')
            f_hsize = int(house_size) + 1
            phil_no = request.POST.get('phil_no')
            hospno = request.POST.get('walkin')
            uis_add = UIS(date = date_today,hospno = hospno,phil_no=phil_no,total_income = tot_income,total_expense = tot_expense,category=category,householdsize = f_hsize)
            uis_add.save()
            if uis_add.uis:
                uis_id = UIS.objects.get(uis = uis_add.uis)
                # informant
                a = Informant(uis=uis_id,date_of_intake = date_today,time_of_interview=time_today,end_time_of_interview=time_end,fullname=noi,relation_to_patient = rtp,contact_number = cnums,address = pa)
                a.save()
                    
                #identifying information
                cn = request.POST.get('cn')
                sx = request.POST.get('gender')
                bdey = request.POST.get('bdate')
                age = request.POST.get('age')
                cs = request.POST.get('cs')
                rel = request.POST.get('rel')
                nat = request.POST.get('nat')
                hea = request.POST.get('hea')
                occu = request.POST.get('occu')
                mi = request.POST.get('mi')
                pt = request.POST.get('pt')
                pob = request.POST.get('pob')
                pea = request.POST.get('pea')
                pra = request.POST.get('pra')
                b = IdentifyingInformation(uis=uis_id,client_name = cn,gender=sx,dob = bdey,age=age,cstat = cs,religion = rel,nationality = nat,hea=hea,occupation = occu,mi=mi,patient_type=pt,pob=pob,permanent_address=pea,present_address=pra)
                b.save()

                #family composition
                fam_com = request.POST.get('familycom')
                  
                if fam_com:
                    fam_data = json.loads(fam_com)
                    for f in fam_data:
                        cname = f['cname']
                        fcgender = f['gender']
                        fccstat = f['cstat']
                        fcrtp = f['rtp']
                        fchea = f['hea']
                        fcoccu = f['occu']
                        fcmi = f['mi']
                        fcage = f['fage']
                        c = FamilyComposition(uis=uis_id,fullname = cname,gender=fcgender,cstat = fccstat,relation_to_patient = fcrtp,hea=fchea,occupation=fcoccu,mi=fcmi,age=fcage)
                        c.save()
                        fc_id = FamilyComposition.objects.get(familyComposition = c.familyComposition)
                elif fam_com == '' or fam_com is None:
                    c = FamilyComposition(uis=uis_id,fullname = cn,gender=sx,cstat = cs,relation_to_patient = "SELF", hea=hea,occupation=occu,mi=mi,age=age)
                    c.save()
                    fc_id = FamilyComposition.objects.get(familyComposition = c.familyComposition)
                else:
                    fam_data = []
                fam_com_osof = request.POST.get('familycomosof')
                if fam_com_osof:
                    famosof_data = json.loads(fam_com_osof)
                    for y in famosof_data:
                        desc_osof = y['desc_osof']
                        amt_osof = y['amt_osof']
                        x = Fc_other_source(uis=uis_id,familyComposition = fc_id,otherSources_of_fi_desc = desc_osof,otherSources_of_fi=amt_osof)
                        x.save()
                else:
                    famosof_data = []

                # #list of expenses
                le_house = request.POST.get('le_house')
                le_amt_house = request.POST.get('le_amt_house')
                le_lot = request.POST.get('le_lot')
                le_amt_lot =request.POST.get('le_amt_lot')
                light_source = []
                water_source = []
                other_expenses = []
                desc_light_source = []
                desc_water_source = []
                desc_others_expenses = []
                prob_presented = []
                prob_presented_desc=[]

                elec = request.POST.get('elec', False)
                amt_elec_init = request.POST.get('amt_elec')
                kero = request.POST.get('kero', False)
                amt_kero_init = request.POST.get('amt_kero')
                cand = request.POST.get('cand', False)
                amt_cand_init = request.POST.get('amt_cand')
                oth = request.POST.get('oth', False)
                amt_oth_init = request.POST.get('amt_oth')
                if elec:
                    desc_elec = "ELECTRICITY"
                    amt_elec = float(amt_elec_init)
                else:
                    desc_elec = ""
                    amt_elec = 0
                    pass
                if kero:
                    desc_kero = "KEROSENE"
                    amt_kero = float(amt_kero_init)
                else:
                    desc_kero = ""
                    amt_kero = 0
                    pass
                if cand:
                    desc_cand = "CANDLE"
                    amt_cand = float(amt_cand_init)
                else:
                    desc_cand = ""
                    amt_cand = 0
                    pass
                if oth:
                    desc_oth = "OTHERS"
                    amt_oth = float(amt_oth_init)
                else:
                    desc_oth = ""
                    amt_oth = 0
                desc_light_source = [desc_elec,desc_kero,desc_cand,desc_oth]
                light_source= [amt_elec,amt_kero,amt_cand,amt_oth]
                        
                water_source_public = request.POST.get('pub', False)
                amt_water_source_public_init = request.POST.get('amt_pub')
                water_source_nat = request.POST.get('natu', False)
                amt_water_source_nat_init = request.POST.get('amt_nat')
                water_source_wd = request.POST.get('wd', False)
                amt_water_source_wd_init = request.POST.get('amt_wd')
                water_source_min = request.POST.get('min', False)
                amt_water_source_min_init = request.POST.get('amt_min')
                if water_source_public:
                    desc_public = "PUBLIC"
                    amt_water_source_public = float(amt_water_source_public_init) 
                else:
                    desc_public = ""
                    amt_water_source_public = 0
                    pass
                if water_source_nat:
                    desc_natural = "NATURAL"
                    amt_water_source_nat = float(amt_water_source_nat_init)
                else:
                    desc_natural = ""
                    amt_water_source_nat = 0
                    pass
                if water_source_wd:
                    desc_wd = "WATER DISTRICT"
                    amt_water_source_wd =  float(amt_water_source_wd_init)
                else:
                    desc_wd = ""
                    amt_water_source_wd = 0
                    pass
                if water_source_min:
                    desc_min = "MINERAL"
                    amt_water_source_min = float(amt_water_source_min_init)
                else:
                    desc_min = ""
                    amt_water_source_min = 0
                desc_water_source=[desc_public,desc_natural,desc_wd,desc_min]
                water_source = [amt_water_source_public,amt_water_source_nat,amt_water_source_wd,amt_water_source_min]
                        
                house = request.POST.get('house', False)
                amt_house_init = request.POST.get('amt_house')
                me = request.POST.get('me', False)
                amt_me_init = request.POST.get('amt_me')
                ip = request.POST.get('ip', False)
                amt_ip_init = request.POST.get('amt_ip')
                edu = request.POST.get('edu', False)
                amt_edu_init = request.POST.get('amt_edu')
                loan = request.POST.get('loan', False)
                amt_loan_init = request.POST.get('amt_loan')
                transpo = request.POST.get('transpo', False)
                amt_transpo_init = request.POST.get('amt_transpo')
                food = request.POST.get('food', False)
                amt_food_init = request.POST.get('amt_food')
                saving = request.POST.get('saving', False)
                amt_saving_init = request.POST.get('amt_saving')
                other = request.POST.get('other', False)
                amt_other_init = request.POST.get('amt_other')
                if house:
                    desc_house = "HOUSE"
                    amt_house = float(amt_house_init)
                else:
                    desc_house = ""
                    amt_house = 0
                    pass
                if me:
                    desc_me = "ME"
                    amt_me = float(amt_me_init)
                else:
                    desc_me = ""
                    amt_me = 0
                    pass
                if ip:
                    desc_ip = "IP"
                    amt_ip = float(amt_ip_init)
                else:
                    desc_ip = ""
                    amt_ip = 0
                    pass
                if edu:
                    desc_edu = "EDU"
                    amt_edu = float(amt_edu_init)
                else:
                    desc_edu = ""
                    amt_edu = 0
                    pass
                if loan:
                    desc_loan = "LOAN"
                    amt_loan = float(amt_loan_init)
                else:
                    desc_loan = ""
                    amt_loan = 0
                    pass
                if transpo:
                    desc_transpo = "TRANSPO"
                    amt_transpo = float(amt_transpo_init)
                else:
                    desc_transpo = ""
                    amt_transpo = 0
                    pass
                if food:
                    desc_food = "FOOD"
                    amt_food = float(amt_food_init)
                else:
                    desc_food=""
                    amt_food = 0
                    pass
                if saving:
                    desc_saving="SAVINGS"
                    amt_saving = float(amt_saving_init)
                else:
                    desc_saving=""
                    amt_saving = 0
                    pass
                if other:
                    desc_other = "OTHER"
                    amt_other = float(amt_other_init)
                else:
                    desc_other = ""
                    amt_other = 0
                desc_others_expenses = [desc_house,desc_me,desc_ip,desc_edu,desc_loan,desc_transpo,desc_food,desc_saving,desc_other]
                other_expenses = [amt_house,amt_me,amt_ip,amt_edu,amt_loan,amt_transpo,amt_food,amt_saving,amt_other]
                d = ListofExpenses(uis = uis_id, house = le_house,amt_house = le_amt_house,lot=le_lot,amt_lot=le_amt_lot,ligth_source=desc_light_source,amt_ligth_source = light_source,water_source=desc_water_source,amt_water_source = water_source,other_expenses=desc_others_expenses,amt_other_expenses = other_expenses)
                d.save()

                # # #problem Presented

                hcop = request.POST.get('hcop', False)
                hcop_desc = request.POST.get('hcop_desc')
                fn = request.POST.get('fn', False)
                fn_desc = request.POST.get('fn_desc')
                emp = request.POST.get('emp', False)
                emp_desc = request.POST.get('emp_desc')
                ers = request.POST.get('ers', False)
                ers_desc = request.POST.get('ers_desc')
                hs = request.POST.get('hs', False)
                hs_desc = request.POST.get('hs_desc')
                osy = request.POST.get('osy', False)
                osy_desc = request.POST.get('osy_desc')
                if hcop:
                    n_hcop = "HCOP"
                    hcop_desc = hcop_desc
                else:
                    n_hcop = ''
                    hcop_desc=''

                if fn:
                    n_fn = "FN"
                    fn_desc = fn_desc
                else:
                    n_fn = ''
                    fn_desc=''
                if emp:
                    n_emp = "EMP"
                    emp_desc = emp_desc
                else:
                    n_emp = ''
                    emp_desc=''
                if ers:
                    n_ers = "ERS"
                    ers_desc = ers_desc
                else:
                    n_ers=''
                    ers_desc=''
                if hs:
                    n_hs = "HS"
                    hs_desc = hs_desc
                else:
                    n_hs = ''
                    hs_desc=''
                if osy:
                    n_osy = 'OSY'
                    osy_desc = osy_desc
                else:
                    n_osy = ''
                    osy_desc=''
                prob_presented = [n_hcop,n_fn,n_emp,n_ers,n_hs,n_osy]
                prob_presented_desc = [hcop_desc,fn_desc,emp_desc,ers_desc,hs_desc,osy_desc]
                e = ProblemPresented(uis = uis_id,problem= prob_presented,prob_desc = prob_presented_desc)
                e.save()

                #swa
                swa = request.POST.get('swa')
                f = SWA(uis = uis_id,swa_desc = swa)
                f.save()

                # reccomendations
                reccomendations = request.POST.get('reccomdata')
                if reccomendations:
                    reccom_data = json.loads(reccomendations)
                    for r in reccom_data:
                        mtoa = r['mtoa']
                        maos = r['maos']
                        mmoa = r['mmoa']
                        mfs = r['mfs']
                        g = Recommendations(uis = uis_id,type_of_assistance = mtoa,amt_of_assistance = maos,mode_of_assistance = mmoa,fund_source = mfs)
                        g.save()
                else:
                    reccom_data = []
                mssatcheck = request.POST.get('mssatcheck',False)
                if mssatcheck:
                    fuel_src = []
                    amt_fuel_src = []
                    doac = request.POST.get('doac')
                    basic_ward = request.POST.get('basic_ward')
                    non_basic = request.POST.get('non_basic')
                    mss_no = request.POST.get('mss_no')
                    src_referal_name = request.POST.get('src_referal_name')
                    cnum = request.POST.get('cnum')
                    address = request.POST.get('address')
                    employer = request.POST.get('employer')
                    tla = request.POST.get('tla')
                    phil_mem = request.POST.get('phil_mem')
                    mswd_cassif = request.POST.get('mswd_cassif')
                    marginalized_sec_mem = request.POST.get('marginalized_sec_mem')
                    clothing_amt = request.POST.get('clothing_amt')
                    duration_of_prob = request.POST.get('duration_of_prob')
                    prev_treatment = request.POST.get('prev_treatment')
                    health_accessibility_prob = request.POST.get('health_accessibility_prob')
                    lpg = request.POST.get('lpg', False)
                    amt_lpg = request.POST.get('amt_lpg')
                    elec = request.POST.get('elec', False)
                    amt_elec = request.POST.get('m_amt_elec')
                    char = request.POST.get('char', False)
                    amt_char = request.POST.get('amt_char')
                    fwood = request.POST.get('fwood', False)
                    amt_fwood = request.POST.get('amt_fwood')
                    if lpg:
                        f_lpg = "LPG"
                        f_amt_lpg =float(amt_lpg)
                    else:
                        f_lpg = ""
                        f_amt_lpg = 0
                        pass
                    if elec:
                        f_elec = "ELECTRICITY"
                        f_amt_elec =float(amt_elec)
                    else:
                        f_elec = ""
                        f_amt_elec = 0
                        pass
                    if char:
                        f_char = "CHARCOAL"
                        f_amt_char =float(amt_char)
                    else:
                        f_char = ""
                        f_amt_char = 0
                        pass
                    if fwood:
                        f_fwood = "FIREWOOD"
                        f_amt_fwood =float(amt_fwood)
                    else:
                        f_fwood = ""
                        f_amt_fwood = 0
                    fuel_src = [f_lpg,f_elec,f_char,f_fwood]
                    amt_fuel_src = [f_amt_lpg,f_amt_elec,f_amt_char,f_amt_fwood]
                    aa = MSSAT(uis=uis_id,doac = doac,basic_ward=basic_ward,non_basic = non_basic,mss_no=mss_no,tla=tla,src_referal_name=src_referal_name,address=address,cnum=cnum,employer=employer,phil_mem=phil_mem,mswd_cassif=mswd_cassif,marginalized_sec_mem=marginalized_sec_mem,fuel_source = fuel_src,amt_fuel_source = amt_fuel_src,clothing_amt=clothing_amt,duration_of_prob=duration_of_prob,prev_treatment=prev_treatment,health_accessibility_prob=health_accessibility_prob)
                    aa.save()
                else:
                    mssatcheck = []
                    pass
                    
                if mssatcheck:
                        
                    upd_has_mssat = UIS.objects.get(uis = uis_add.uis)
                    upd_has_mssat.has_mssat = True
                    upd_has_mssat.save()
                    redirect_url_with_args = f'/{uis_id}/mssat_pdf'
                else:
                    redirect_url_with_args = f'/{uis_id}/uis_pdf'
                messages.success(request, "SUCCESSFULLY ADDED")
                return redirect(redirect_url_with_args)
        return HttpResponseRedirect("/uis_list")
    else:
        return HttpResponseRedirect("/auth_login")

def duplicate_uis(request,uis):
    if request.session.get('employee_id') is not None:
        showRCD = requests.post(malasakit_api_showRCD).json()
        now = datetime.now()
        date_today = datetime.strftime(now, '%Y-%m-%d')
        time_today = datetime.strftime(now,'%I:%M %p')
        time_started = datetime.strftime(now,'%I:%M %p')
        request.session['start_time_dupuis'] = time_started
        if showRCD['status'] == 'success':
            get_rcd  = showRCD['data']
        try:
            uis_details = UIS.objects.get(uis=uis)
            informant  = Informant.objects.get(uis=uis)
            iden_info = IdentifyingInformation.objects.get(uis=uis)
            loe= ListofExpenses.objects.get(uis=uis)
            conv_ls = loe.ligth_source.replace("[","").replace("]","").replace("'","")
            conv_ls_space = conv_ls.replace(" ","")
            new_ls = conv_ls_space.split(',')
            conv_ls_amt = loe.amt_ligth_source.replace("[","").replace("]","").replace("'","")
            conv_ls_space_amt = conv_ls_amt.replace(" ","")
            new_ls_amt = conv_ls_space_amt.split(',')
            conv_ws = loe.water_source.replace("[","").replace("]","").replace("'","")
            conv_ws_space = conv_ws.replace(" ","")
            new_ws  = conv_ws_space.split(',')
            conv_ws_amt = loe.amt_water_source.replace("[","").replace("]","").replace("'","")
            conv_ws_space_amt = conv_ws_amt.replace(" ","")
            new_ws_amt = conv_ws_space_amt.split(',')
            conv_other_expenses = loe.other_expenses.replace("[","").replace("]","").replace("'","")
            conv_other_expenses_space = conv_other_expenses.replace(" ","")
            new_oe = conv_other_expenses_space.split(',')

            conv_other_expenses_amt = loe.amt_other_expenses.replace("[","").replace("]","").replace("'","")
            conv_other_expenses_space_amt = conv_other_expenses_amt.replace(" ","")
            new_amt_oe = conv_other_expenses_space_amt.split(',')

            mm = ProblemPresented.objects.get(uis = uis)
            probpres_id = mm.problemPresented
            problem = mm.problem
            conv_problem = problem.replace("[","").replace("]","").replace("'","")
            f_problem = conv_problem.replace(" ","")
            fproblem = f_problem.split(',')
            prob_desc = mm.prob_desc
            conv_prob_desc = prob_desc.replace("[","").replace("]","").replace("'","")
            f_prob_desc = conv_prob_desc.split(',') 

            swa_desc = SWA.objects.get(uis = uis)

            famcom = FamilyComposition.objects.filter(uis = uis)
            mi_tot = 0
            for c in famcom:
                mi_tot += float(c.mi)
            num_famcom = FamilyComposition.objects.filter(uis = uis).count()
            famcom_osof = Fc_other_source.objects.filter(uis = uis)
            osof_amt_tot = 0
            for b in famcom_osof:
                if b.otherSources_of_fi_desc == 'CCT':
                    amt_osof = float(b.otherSources_of_fi)/2
                else:
                    amt_osof = float(b.otherSources_of_fi)
                osof_amt_tot += amt_osof
            # print(osof_amt_tot)
            dup_datas =FamilyComposition.objects.filter(uis = uis)
            dup_osof_datas =Fc_other_source.objects.filter(uis = uis)
            reccom = Recommendations.objects.filter(uis = uis)
        except uis_details.DoesNotExist:
            raise Http404("Patient Doest not exist")
        return render(request, 'uis/duplicate_uis.html',{'dup_osof_datas':dup_osof_datas,'dup_datas':dup_datas,'time_today':request.session['start_time_dupuis'],'date_today':date_today,'get_rcd':get_rcd,'probpres_id':probpres_id,'id_uis':uis,'osof_amt_tot':osof_amt_tot,'mi_tot':mi_tot,'num_famcom':num_famcom,'reccom':reccom,'famcom_osof':famcom_osof,'famcom':famcom,'swa_desc':swa_desc,'f_prob_desc':f_prob_desc,'fproblem':fproblem,'new_amt_oe':new_amt_oe,'new_oe':new_oe,'amt_ws':new_ws_amt,'ws':new_ws,'amt_ls':new_ls_amt,'ls':new_ls,'loe':loe,'iden_info':iden_info ,'uis_details':uis_details,'informant':informant,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")

def process_duplicate_uis(request):
    if request.session.get('employee_id') is not None:
        now = datetime.now()
        complain = ""
        if request.method == 'POST':
            date_today = datetime.strftime(now, '%Y-%m-%d')
            time_end = datetime.strftime(now,'%I:%M %p')
            time_today = request.session['start_time_dupuis']
            
            #informant data
            noi = request.POST.get('noi').upper()
            rtp = request.POST.get('rtp').upper()
            cnums = request.POST.get('cnums')
            pa = request.POST.get('pa').upper()
            tot_income = request.POST.get('tot_income')
            tot_expense = request.POST.get('tot_expense')
            category = request.POST.get('klass')
            house_size = request.POST.get('housize')
            f_hsize = int(house_size) + 1
            phil_no = request.POST.get('phil_no')
            hospno = request.POST.get('dup_uis_hospono')
            uis_add = UIS(date = date_today,hospno = hospno,phil_no=phil_no,total_income = tot_income,total_expense = tot_expense,category=category,householdsize = f_hsize)
            uis_add.save()
            if uis_add.uis:
                uis_id = UIS.objects.get(uis = uis_add.uis)
                # informant
                a = Informant(uis=uis_id,date_of_intake = date_today,time_of_interview=time_today,end_time_of_interview=time_end,fullname=noi,relation_to_patient = rtp,contact_number = cnums,address = pa)
                a.save()
                    
                #identifying information
                cn = request.POST.get('cn')
                sx = request.POST.get('gender')
                bdey = request.POST.get('bdate')
                age = request.POST.get('age')
                cs = request.POST.get('cs')
                rel = request.POST.get('rel')
                nat = request.POST.get('nat')
                hea = request.POST.get('hea')
                occu = request.POST.get('occu')
                mi = request.POST.get('mi')
                pt = request.POST.get('pt')
                pob = request.POST.get('pob')
                pea = request.POST.get('pea')
                pra = request.POST.get('pra')
                b = IdentifyingInformation(uis=uis_id,client_name = cn,gender=sx,dob = bdey,age=age,cstat = cs,religion = rel,nationality = nat,hea=hea,occupation = occu,mi=mi,patient_type=pt,pob=pob,permanent_address=pea,present_address=pra)
                b.save()

                #family composition
                fam_com = request.POST.get('familycom')
                  
                if fam_com:
                    fam_data = json.loads(fam_com)
                    for f in fam_data:
                        cname = f['cname']
                        fcgender = f['gender']
                        fccstat = f['cstat']
                        fcrtp = f['rtp']
                        fchea = f['hea']
                        fcoccu = f['occu']
                        fcmi = f['mi']
                        fcage = f['fage']
                        c = FamilyComposition(uis=uis_id,fullname = cname,gender=fcgender,cstat = fccstat,relation_to_patient = fcrtp,hea=fchea,occupation=fcoccu,mi=fcmi,age=fcage)
                        c.save()
                        fc_id = FamilyComposition.objects.get(familyComposition = c.familyComposition)
                elif fam_com == '' or fam_com is None:
                    c = FamilyComposition(uis=uis_id,fullname = cn,gender=sx,cstat = cs,relation_to_patient = "SELF", hea=hea,occupation=occu,mi=mi,age=age)
                    c.save()
                    fc_id = FamilyComposition.objects.get(familyComposition = c.familyComposition)
                else:
                    fam_data = []
                fam_com_osof = request.POST.get('familycomosof')
                if fam_com_osof:
                    famosof_data = json.loads(fam_com_osof)
                    for y in famosof_data:
                        desc_osof = y['desc_osof']
                        amt_osof = y['amt_osof']
                        x = Fc_other_source(uis=uis_id,familyComposition = fc_id,otherSources_of_fi_desc = desc_osof,otherSources_of_fi=amt_osof)
                        x.save()
                else:
                    famosof_data = []

                # #list of expenses
                le_house = request.POST.get('le_house')
                le_amt_house = request.POST.get('le_amt_house')
                le_lot = request.POST.get('le_lot')
                le_amt_lot =request.POST.get('le_amt_lot')
                light_source = []
                water_source = []
                other_expenses = []
                desc_light_source = []
                desc_water_source = []
                desc_others_expenses = []
                prob_presented = []
                prob_presented_desc=[]

                elec = request.POST.get('elec', False)
                amt_elec_init = request.POST.get('amt_elec')
                kero = request.POST.get('kero', False)
                amt_kero_init = request.POST.get('amt_kero')
                cand = request.POST.get('cand', False)
                amt_cand_init = request.POST.get('amt_cand')
                oth = request.POST.get('oth', False)
                amt_oth_init = request.POST.get('amt_oth')
                if elec:
                    desc_elec = "ELECTRICITY"
                    amt_elec = float(amt_elec_init)
                else:
                    desc_elec = ""
                    amt_elec = 0
                    pass
                if kero:
                    desc_kero = "KEROSENE"
                    amt_kero = float(amt_kero_init)
                else:
                    desc_kero = ""
                    amt_kero = 0
                    pass
                if cand:
                    desc_cand = "CANDLE"
                    amt_cand = float(amt_cand_init)
                else:
                    desc_cand = ""
                    amt_cand = 0
                    pass
                if oth:
                    desc_oth = "OTHERS"
                    amt_oth = float(amt_oth_init)
                else:
                    desc_oth = ""
                    amt_oth = 0
                desc_light_source = [desc_elec,desc_kero,desc_cand,desc_oth]
                light_source= [amt_elec,amt_kero,amt_cand,amt_oth]
                        
                water_source_public = request.POST.get('pub', False)
                amt_water_source_public_init = request.POST.get('amt_pub')
                water_source_nat = request.POST.get('natu', False)
                amt_water_source_nat_init = request.POST.get('amt_nat')
                water_source_wd = request.POST.get('wd', False)
                amt_water_source_wd_init = request.POST.get('amt_wd')
                water_source_min = request.POST.get('min', False)
                amt_water_source_min_init = request.POST.get('amt_min')
                if water_source_public:
                    desc_public = "PUBLIC"
                    amt_water_source_public = float(amt_water_source_public_init) 
                else:
                    desc_public = ""
                    amt_water_source_public = 0
                    pass
                if water_source_nat:
                    desc_natural = "NATURAL"
                    amt_water_source_nat = float(amt_water_source_nat_init)
                else:
                    desc_natural = ""
                    amt_water_source_nat = 0
                    pass
                if water_source_wd:
                    desc_wd = "WATER DISTRICT"
                    amt_water_source_wd =  float(amt_water_source_wd_init)
                else:
                    desc_wd = ""
                    amt_water_source_wd = 0
                    pass
                if water_source_min:
                    desc_min = "MINERAL"
                    amt_water_source_min = float(amt_water_source_min_init)
                else:
                    desc_min = ""
                    amt_water_source_min = 0
                desc_water_source=[desc_public,desc_natural,desc_wd,desc_min]
                water_source = [amt_water_source_public,amt_water_source_nat,amt_water_source_wd,amt_water_source_min]
                        
                house = request.POST.get('house', False)
                amt_house_init = request.POST.get('amt_house')
                me = request.POST.get('me', False)
                amt_me_init = request.POST.get('amt_me')
                ip = request.POST.get('ip', False)
                amt_ip_init = request.POST.get('amt_ip')
                edu = request.POST.get('edu', False)
                amt_edu_init = request.POST.get('amt_edu')
                loan = request.POST.get('loan', False)
                amt_loan_init = request.POST.get('amt_loan')
                transpo = request.POST.get('transpo', False)
                amt_transpo_init = request.POST.get('amt_transpo')
                food = request.POST.get('food', False)
                amt_food_init = request.POST.get('amt_food')
                saving = request.POST.get('saving', False)
                amt_saving_init = request.POST.get('amt_saving')
                other = request.POST.get('other', False)
                amt_other_init = request.POST.get('amt_other')
                if house:
                    desc_house = "HOUSE"
                    amt_house = float(amt_house_init)
                else:
                    desc_house = ""
                    amt_house = 0
                    pass
                if me:
                    desc_me = "ME"
                    amt_me = float(amt_me_init)
                else:
                    desc_me = ""
                    amt_me = 0
                    pass
                if ip:
                    desc_ip = "IP"
                    amt_ip = float(amt_ip_init)
                else:
                    desc_ip = ""
                    amt_ip = 0
                    pass
                if edu:
                    desc_edu = "EDU"
                    amt_edu = float(amt_edu_init)
                else:
                    desc_edu = ""
                    amt_edu = 0
                    pass
                if loan:
                    desc_loan = "LOAN"
                    amt_loan = float(amt_loan_init)
                else:
                    desc_loan = ""
                    amt_loan = 0
                    pass
                if transpo:
                    desc_transpo = "TRANSPO"
                    amt_transpo = float(amt_transpo_init)
                else:
                    desc_transpo = ""
                    amt_transpo = 0
                    pass
                if food:
                    desc_food = "FOOD"
                    amt_food = float(amt_food_init)
                else:
                    desc_food=""
                    amt_food = 0
                    pass
                if saving:
                    desc_saving="SAVINGS"
                    amt_saving = float(amt_saving_init)
                else:
                    desc_saving=""
                    amt_saving = 0
                    pass
                if other:
                    desc_other = "OTHER"
                    amt_other = float(amt_other_init)
                else:
                    desc_other = ""
                    amt_other = 0
                desc_others_expenses = [desc_house,desc_me,desc_ip,desc_edu,desc_loan,desc_transpo,desc_food,desc_saving,desc_other]
                other_expenses = [amt_house,amt_me,amt_ip,amt_edu,amt_loan,amt_transpo,amt_food,amt_saving,amt_other]
                d = ListofExpenses(uis = uis_id, house = le_house,amt_house = le_amt_house,lot=le_lot,amt_lot=le_amt_lot,ligth_source=desc_light_source,amt_ligth_source = light_source,water_source=desc_water_source,amt_water_source = water_source,other_expenses=desc_others_expenses,amt_other_expenses = other_expenses)
                d.save()

                # # #problem Presented

                hcop = request.POST.get('hcop', False)
                hcop_desc = request.POST.get('hcop_desc')
                fn = request.POST.get('fn', False)
                fn_desc = request.POST.get('fn_desc')
                emp = request.POST.get('emp', False)
                emp_desc = request.POST.get('emp_desc')
                ers = request.POST.get('ers', False)
                ers_desc = request.POST.get('ers_desc')
                hs = request.POST.get('hs', False)
                hs_desc = request.POST.get('hs_desc')
                osy = request.POST.get('osy', False)
                osy_desc = request.POST.get('osy_desc')
                if hcop:
                    n_hcop = "HCOP"
                    hcop_desc = hcop_desc
                else:
                    n_hcop = ''
                    hcop_desc=''

                if fn:
                    n_fn = "FN"
                    fn_desc = fn_desc
                else:
                    n_fn = ''
                    fn_desc=''
                if emp:
                    n_emp = "EMP"
                    emp_desc = emp_desc
                else:
                    n_emp = ''
                    emp_desc=''
                if ers:
                    n_ers = "ERS"
                    ers_desc = ers_desc
                else:
                    n_ers=''
                    ers_desc=''
                if hs:
                    n_hs = "HS"
                    hs_desc = hs_desc
                else:
                    n_hs = ''
                    hs_desc=''
                if osy:
                    n_osy = 'OSY'
                    osy_desc = osy_desc
                else:
                    n_osy = ''
                    osy_desc=''
                prob_presented = [n_hcop,n_fn,n_emp,n_ers,n_hs,n_osy]
                prob_presented_desc = [hcop_desc,fn_desc,emp_desc,ers_desc,hs_desc,osy_desc]
                e = ProblemPresented(uis = uis_id,problem= prob_presented,prob_desc = prob_presented_desc)
                e.save()

                #swa
                swa = request.POST.get('swa')
                f = SWA(uis = uis_id,swa_desc = swa)
                f.save()

                # reccomendations
                reccomendations = request.POST.get('reccomdata')
                if reccomendations:
                    reccom_data = json.loads(reccomendations)
                    for r in reccom_data:
                        mtoa = r['mtoa']
                        maos = r['maos']
                        mmoa = r['mmoa']
                        mfs = r['mfs']
                        g = Recommendations(uis = uis_id,type_of_assistance = mtoa,amt_of_assistance = maos,mode_of_assistance = mmoa,fund_source = mfs)
                        g.save()
                else:
                    reccom_data = []
                mssatcheck = request.POST.get('mssatcheck',False)
                if mssatcheck:
                    fuel_src = []
                    amt_fuel_src = []
                    doac = request.POST.get('doac')
                    basic_ward = request.POST.get('basic_ward')
                    non_basic = request.POST.get('non_basic')
                    mss_no = request.POST.get('mss_no')
                    src_referal_name = request.POST.get('src_referal_name')
                    cnum = request.POST.get('cnum')
                    address = request.POST.get('address')
                    employer = request.POST.get('employer')
                    tla = request.POST.get('tla')
                    phil_mem = request.POST.get('phil_mem')
                    mswd_cassif = request.POST.get('mswd_cassif')
                    marginalized_sec_mem = request.POST.get('marginalized_sec_mem')
                    clothing_amt = request.POST.get('clothing_amt')
                    duration_of_prob = request.POST.get('duration_of_prob')
                    prev_treatment = request.POST.get('prev_treatment')
                    health_accessibility_prob = request.POST.get('health_accessibility_prob')
                    lpg = request.POST.get('lpg', False)
                    amt_lpg = request.POST.get('amt_lpg')
                    elec = request.POST.get('elec', False)
                    amt_elec = request.POST.get('m_amt_elec')
                    char = request.POST.get('char', False)
                    amt_char = request.POST.get('amt_char')
                    fwood = request.POST.get('fwood', False)
                    amt_fwood = request.POST.get('amt_fwood')
                    if lpg:
                        f_lpg = "LPG"
                        f_amt_lpg =float(amt_lpg)
                    else:
                        f_lpg = ""
                        f_amt_lpg = 0
                        pass
                    if elec:
                        f_elec = "ELECTRICITY"
                        f_amt_elec =float(amt_elec)
                    else:
                        f_elec = ""
                        f_amt_elec = 0
                        pass
                    if char:
                        f_char = "CHARCOAL"
                        f_amt_char =float(amt_char)
                    else:
                        f_char = ""
                        f_amt_char = 0
                        pass
                    if fwood:
                        f_fwood = "FIREWOOD"
                        f_amt_fwood =float(amt_fwood)
                    else:
                        f_fwood = ""
                        f_amt_fwood = 0
                    fuel_src = [f_lpg,f_elec,f_char,f_fwood]
                    amt_fuel_src = [f_amt_lpg,f_amt_elec,f_amt_char,f_amt_fwood]
                    aa = MSSAT(uis=uis_id,doac = doac,basic_ward=basic_ward,non_basic = non_basic,mss_no=mss_no,tla=tla,src_referal_name=src_referal_name,address=address,cnum=cnum,employer=employer,phil_mem=phil_mem,mswd_cassif=mswd_cassif,marginalized_sec_mem=marginalized_sec_mem,fuel_source = fuel_src,amt_fuel_source = amt_fuel_src,clothing_amt=clothing_amt,duration_of_prob=duration_of_prob,prev_treatment=prev_treatment,health_accessibility_prob=health_accessibility_prob)
                    aa.save()
                else:
                    mssatcheck = []
                    pass
                    
                if mssatcheck:
                        
                    upd_has_mssat = UIS.objects.get(uis = uis_add.uis)
                    upd_has_mssat.has_mssat = True
                    upd_has_mssat.save()
                    redirect_url_with_args = f'/{uis_id}/mssat_pdf'
                else:
                    redirect_url_with_args = f'/{uis_id}/uis_pdf'
                messages.success(request, "SUCCESSFULLY ADDED")
                return redirect(redirect_url_with_args)
        return HttpResponseRedirect("/uis_list")
    else:
        return HttpResponseRedirect("/auth_login")

def delete_uis(request, uis_id):
    UIS.objects.filter(uis=uis_id).delete()
    return HttpResponseRedirect('/uis_list')