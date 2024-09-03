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
from .. import uis_pdf
from django.db.models import ProtectedError, RestrictedError
import pandas as pd
from openpyxl.workbook import Workbook
from openpyxl import load_workbook


root = "http://173.10.2.108:9092/"
# root = "http://172.22.10.11:9091/"
cashop_api = root + "api/cashop/lookup"
login_api = root + "api/login"
cashop_api_ecntr = root + "api/cashop/encounter"
malasakit_patiet_details = root + "api/malasakit/patient-details"
malasakit_api_showRCD= root + "api/cashop/showRCD"
malasakit_api_adm_patient = root + "api/adm/admlist"



def get_patient_history(request,hospno,code, toecode):
    if request.session.get('employee_id') is not None:
        complain = ""
        codes = code.replace("-","/")
        results = requests.post(malasakit_patiet_details,data = {'enccode': code}).json()
        if results['status'] == 'success':
            get_complaint = results['data']['complaint']
            for cc in get_complaint:
                complain = cc['history']
                if toecode == 'ADM':
                 
                    show_admlist = requests.post(malasakit_api_adm_patient).json()
                    if show_admlist['status'] == 'success':
                        get_adm_patient = show_admlist['data']
                        for i in get_adm_patient:
                            if i['enccode'] == codes and i['hpercode'] == hospno:
                                
                                request.session['complain'] = i['admtxt']
                else:
                    request.session['complain'] = complain
        results = requests.post(cashop_api,data = {'hospno': hospno}).json()
        get_results_name = results['data']
        for ii in get_results_name:
            fullname = ii['patfirst']+" "+ii['patmiddle']+" "+ii['patlast']
        try:
            uis  = UIS.objects.get(hospno = hospno)
            informant = Informant.objects.filter(uis=uis.uis)
            if request.session['complain'] == 'ADMITTED':
                    show_admlist = requests.post(malasakit_api_adm_patient).json()
                    if show_admlist['status'] == 'success':
                        get_adm_patient = show_admlist['data']
                        for i in get_adm_patient:
                            if i['enccode'] == codes and i['hpercode'] == hospno:
                                request.session['complain'] = i['admtxt']
            return render(request, 'uis/patient_uis_history.html',{'complain':request.session['complain'],'informant':informant,'code':code,'toecode':toecode, 'hospno':hospno,'fullname':fullname,'user':request.session['name']})
        except ObjectDoesNotExist: 
            if request.session['complain'] == 'ADMITTED':
                    show_admlist = requests.post(malasakit_api_adm_patient).json()
                    if show_admlist['status'] == 'success':
                        get_adm_patient = show_admlist['data']
                        for i in get_adm_patient:
                            if i['enccode'] == codes and i['hpercode'] == hospno:
                                request.session['complain'] = i['admtxt']
            return render(request, 'uis/patient_uis_history.html',{'complain':request.session['complain'],'code':code,'toecode':toecode, 'hospno':hospno,'fullname':fullname,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")

def add_uis(request, hospno,code, toecode): # no record
    if request.session.get('employee_id') is not None:
        now = datetime.now()
        complain = ""
        date_today = datetime.strftime(now, '%Y-%m-%d')
        date_show = datetime.strftime(now, '%b %d, %Y')
        time_show = request.session['start_time']
        time_ended = datetime.strftime(now, '%I:%M %p')
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
                tot_reccom_amt = request.POST.get('tot_reccom_amt')
                try:
                    UIS.objects.get(hospno = hospno)
                    messages.warning(request, "Patient Already exist!")
                    return HttpResponseRedirect('/')
                except ObjectDoesNotExist:
                    uis_add = UIS(date = date_today,hospno = hospno,phil_no=phil_no)
                    uis_add.save()
                    if uis_add.uis:
                        uis_id = UIS.objects.get(uis = uis_add.uis)
                        #
                        uu = UIS_misc(uis = uis_id, total_income = tot_income,total_expense = tot_expense,toe=toecode,category=category, total_amount_of_assistance=tot_reccom_amt,householdsize = f_hsize,swo=request.session['name'])
                        uu.save()
                        uis_misc_id = UIS_misc.objects.get(uis_misc = uu.uis_misc)
                        # informant
                        a = Informant(uis=uis_id,uis_misc = uis_misc_id,date_of_intake = date_today,time_of_interview=time_today,end_time_of_interview=time_end,fullname=noi,relation_to_patient = rtp,contact_number = cnums,address = pa)
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
                        d = ListofExpenses(uis = uis_id,uis_misc = uis_misc_id, house = le_house,amt_house = le_amt_house,lot=le_lot,amt_lot=le_amt_lot,ligth_source=desc_light_source,amt_ligth_source = light_source,water_source=desc_water_source,amt_water_source = water_source,other_expenses=desc_others_expenses,amt_other_expenses = other_expenses)
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
                        e = ProblemPresented(uis = uis_id,uis_misc = uis_misc_id,problem= prob_presented,prob_desc = prob_presented_desc)
                        e.save()

                        #swa
                        swa = request.POST.get('swa')
                        f = SWA(uis = uis_id,uis_misc = uis_misc_id,swa_desc = swa)
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

                                g = Recommendations(uis = uis_id,uis_misc = uis_misc_id,type_of_assistance = mtoa,amt_of_assistance = maos,mode_of_assistance = mmoa,fund_source = mfs)
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
                            print(uis_misc_id)
                            amt_fuel_src = [f_amt_lpg,f_amt_char,f_amt_fwood]
                            aa = MSSAT(uis=uis_id,uis_misc = uis_misc_id,doac = doac,venue=venue,category=categorys,basic_ward=ward,mss_no=mss_no,tla=tla,src_referal_name=src_referal_name,address=address,cnum=cnumba,phil_mem=phil_mem,marginalized_sec_mem=marginalized_sec_mem,fuel_source = fuel_src,amt_fuel_source = amt_fuel_src,clothing_amt=clothing_amt,duration_of_prob=duration_of_prob,prev_treatment=prev_treatment,health_accessibility_prob=health_accessibility_prob)
                            aa.save()

                        else:
                            mssatcheck = []
                        if mssatcheck:
                            upd_has_mssat = UIS_misc.objects.get(uis_misc = uu.uis_misc)
                            upd_has_mssat.has_mssat = True
                            upd_has_mssat.save()
                            redirect_url_with_args = f'/{uis_id}/{uis_misc_id}/new_mssat_pdf'
                        else:
                            redirect_url_with_args = f'/{uis_id}/{uis_misc_id}/uis_pdf'
                        messages.success(request, "SUCCESSFULLY ADDED")
                        return redirect(redirect_url_with_args)
        return render(request, 'uis/add_uis.html',{'time_ended':time_ended,'time_show':time_show,'date_show':date_show,'get_rcd':get_rcd,'mms_no_auto':mms_no_auto,'date_today':date_today,'user':request.session['name'],'complain':request.session['complain'],'toecode':toecode,'age':age,'rel':rel,'nat':nat,'cstat':cstat,'occu':occu,'address':get_address,'pob':pob,'code':code,'hospno':hospno,'fullname':fullname,'gender':gender,'bday':bdate})
    else:
        return HttpResponseRedirect("/auth_login")

def copy_uis(request,uis,uis_misc):
    if request.session.get('employee_id') is not None:
        showRCD = requests.post(malasakit_api_showRCD).json()
        complain=""
        try:
            if request.session['complain']:
                complain= request.session['complain']
            else:
                complain = ""
        except(KeyError):
            complain=""
        if showRCD['status'] == 'success':
            get_rcd  = showRCD['data']
        try:  
            now = datetime.now()
            time_started = datetime.strftime(now, '%I:%M:%S %p')
            request.session['start_time_upduis'] = time_started
            uis_details = UIS.objects.get(uis=uis)
            uis_miscs = UIS_misc.objects.get(uis_misc = uis_misc)
            informant  = Informant.objects.get(uis_misc=uis_misc)
            iden_info = IdentifyingInformation.objects.get(uis=uis)
            loe= ListofExpenses.objects.get(uis_misc=uis_misc)
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

            mm = ProblemPresented.objects.get(uis_misc=uis_misc)
            probpres_id = mm.problemPresented
            problem = mm.problem
            conv_problem = problem.replace("[","").replace("]","").replace("'","")
            f_problem = conv_problem.replace(" ","")
            fproblem = f_problem.split(',')
            prob_desc = mm.prob_desc
            conv_prob_desc = prob_desc.replace("[","").replace("]","").replace("'","")
            f_prob_desc = conv_prob_desc.split(',') 

            swa_desc = SWA.objects.get(uis_misc=uis_misc)

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
            reccom = Recommendations.objects.filter(uis_misc=uis_misc)
        except uis_details.DoesNotExist:
            raise Http404("Patient Doest not exist")
        return render(request, 'uis/copy_uis.html',{'dup_osof_datas':dup_osof_datas,'dup_datas':dup_datas,'complain':complain,'uis_miscs':uis_miscs,'start_time':request.session['start_time_upduis'],'get_rcd':get_rcd,'probpres_id':probpres_id,'id_uis':uis,'id_uis_misc':uis_misc,'osof_amt_tot':osof_amt_tot,'mi_tot':mi_tot,'num_famcom':num_famcom,'reccom':reccom,'famcom_osof':famcom_osof,'famcom':famcom,'swa_desc':swa_desc,'f_prob_desc':f_prob_desc,'fproblem':fproblem,'new_amt_oe':new_amt_oe,'new_oe':new_oe,'amt_ws':new_ws_amt,'ws':new_ws,'amt_ls':new_ls_amt,'ls':new_ls,'loe':loe,'iden_info':iden_info ,'uis_details':uis_details,'informant':informant,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")
def copy_uis_add(request): # no record
    if request.session.get('employee_id') is not None:
        now = datetime.now()
        complain = ""
        date_today = datetime.strftime(now, '%Y-%m-%d')
        date_show = datetime.strftime(now, '%b %d, %Y')
        time_show = request.session['start_time']
        time_ended = datetime.strftime(now, '%I:%M %p')
        mms_no_auto = datetime.strftime(now, '%Y-%m-')
        showRCD = requests.post(malasakit_api_showRCD).json()
        if showRCD['status'] == 'success':
            get_rcd  = showRCD['data']
        if request.method == 'POST':
            date_today = datetime.strftime(now, '%Y-%m-%d')
            time_today =request.session['start_time']
            time_end = datetime.strftime(now,'%I:%M %p')
            #informant data
            hospno = request.POST.get('hosp_num')
            toed = request.POST.get('toed')
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
            tot_reccom_amt = request.POST.get('tot_reccom_amt')
            try:
                UIS.objects.get(hospno = hospno)
                messages.warning(request, "Patient Already exist!")
                return HttpResponseRedirect('/')
            except ObjectDoesNotExist:
                uis_add = UIS(date = date_today,hospno = hospno,phil_no=phil_no)
                uis_add.save()
                if uis_add.uis:
                    uis_id = UIS.objects.get(uis = uis_add.uis)
                    #
                    uu = UIS_misc(uis = uis_id, total_income = tot_income,total_expense = tot_expense,toe=toed,category=category, total_amount_of_assistance=tot_reccom_amt,householdsize = f_hsize,swo=request.session['name'])
                    uu.save()
                    uis_misc_id = UIS_misc.objects.get(uis_misc = uu.uis_misc)
                    # informant
                    a = Informant(uis=uis_id,uis_misc = uis_misc_id,date_of_intake = date_today,time_of_interview=time_today,end_time_of_interview=time_end,fullname=noi,relation_to_patient = rtp,contact_number = cnums,address = pa)
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
                    d = ListofExpenses(uis = uis_id,uis_misc = uis_misc_id, house = le_house,amt_house = le_amt_house,lot=le_lot,amt_lot=le_amt_lot,ligth_source=desc_light_source,amt_ligth_source = light_source,water_source=desc_water_source,amt_water_source = water_source,other_expenses=desc_others_expenses,amt_other_expenses = other_expenses)
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
                    e = ProblemPresented(uis = uis_id,uis_misc = uis_misc_id,problem= prob_presented,prob_desc = prob_presented_desc)
                    e.save()
                    #swa
                    swa = request.POST.get('swa')
                    f = SWA(uis = uis_id,uis_misc = uis_misc_id,swa_desc = swa)
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
                            g = Recommendations(uis = uis_id,uis_misc = uis_misc_id,type_of_assistance = mtoa,amt_of_assistance = maos,mode_of_assistance = mmoa,fund_source = mfs)
                            g.save()
                    else:
                        reccom_data = []
                    redirect_url_with_args = f'/{uis_id}/{uis_misc_id}/uis_pdf'
                    messages.success(request, "SUCCESSFULLY ADDED")
                    return redirect(redirect_url_with_args)
        return HttpResponseRedirect("/uis_list")
    else:
        return HttpResponseRedirect("/auth_login")