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


root = "http://173.10.2.108:9092/"
# root = "http://172.22.10.11:9091/"
cashop_api = root + "api/cashop/lookup"
login_api = root + "api/login"
cashop_api_ecntr = root + "api/cashop/encounter"
malasakit_patiet_details = root + "api/malasakit/patient-details"
malasakit_api_showRCD= root + "api/cashop/showRCD"
def mss_tool_list(request):
    query = request.GET.get('search', '')
    if query:
        uis_show = UIS.objects.all()
        uis_misc = UIS_misc.objects.all()
        show = IdentifyingInformation.objects.filter(Q (client_name__icontains=query))
        mssat_uis = MSSAT.objects.all()
    else:
        uis_show = UIS.objects.all()
        show = IdentifyingInformation.objects.all()[:10]
        uis_misc = UIS_misc.objects.all()
        mssat_uis = MSSAT.objects.all()
    return render(request,'uis/mss_tool_list.html',{'uis_misc':uis_misc,'show':show,'uis':uis_show,'mssat_uis':mssat_uis,'user':request.session['name']})

def get_patient_uis_to_mssat(request,uis,hospno):
    if request.session.get('employee_id') is not None:
        try:
            uis  = UIS.objects.get(hospno = hospno)
            iden = IdentifyingInformation.objects.get(uis=uis)
            fullname = iden.client_name
            informant = Informant.objects.filter(uis=uis.uis)
          
            return render(request, 'uis/patient_uis_mssat.html',{'fullname':fullname,'hospno':hospno,'informant':informant,'user':request.session['name']})
        except ObjectDoesNotExist:
            iden = IdentifyingInformation.objects.get(uis=uis)
            fullname = iden.client_name
            return render(request, 'uis/patient_uis_mssat.html',{'fullname':fullname,'hospno':hospno,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")
    
def get_patient_uis_to_mssat_history(request,uis,hospno):
    if request.session.get('employee_id') is not None:
        try:
            uis_id  = UIS.objects.get(hospno = hospno)
            iden = IdentifyingInformation.objects.get(uis=uis)
            fullname = iden.client_name
            uis_misc = UIS_misc.objects.filter(uis=uis_id.uis,has_mssat=1)
            informant = Informant.objects.filter(uis=uis_id.uis)
            mssat = MSSAT.objects.filter(uis=uis)
          
            return render(request, 'uis/mssat_history.html',{'uis_id':uis,'uis_misc':uis_misc,'mssat':mssat,'fullname':fullname,'hospno':hospno,'informant':informant,'user':request.session['name']})
        except ObjectDoesNotExist:
            return render(request, 'uis/mssat_history.html',{'uis_id':uis,'uis_misc':uis_misc,'informant':informant,'mssat':mssat,'fullname':fullname,'hospno':hospno,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")

def add_mssat(request,uis,misc_uis):
    if request.session.get('employee_id') is not None:
        now = datetime.now()
        date_today = datetime.strftime(now, '%Y-%m-%d')
        mms_no_auto = datetime.strftime(now, '%Y-%m-')
        uis_g = UIS.objects.get(uis=uis)
        time_starts = datetime.strftime(now, '%I:%M %p')
        request.session['mssat_start']= time_starts
        time_endede = datetime.strftime(now, '%I:%M %p')
        info_g = Informant.objects.get(uis_misc=misc_uis)
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
            uis_misc= UIS_misc.objects.get(uis_misc = misc_uis)
            aa = MSSAT(uis=uis_id,uis_misc = uis_misc,doac = doac,venue=venue,category = categorys,basic_ward=ward,mss_no=mss_no,tla=tla,src_referal_name=src_referal_name,address=address,cnum=cnum,phil_mem=phil_mem,marginalized_sec_mem=marginalized_sec_mem,fuel_source = fuel_src,amt_fuel_source = amt_fuel_src,clothing_amt=clothing_amt,duration_of_prob=duration_of_prob,prev_treatment=prev_treatment,health_accessibility_prob=health_accessibility_prob)
            aa.save()
            upd_has_mssat = UIS_misc.objects.get(uis_misc = misc_uis)
            upd_has_mssat.has_mssat = True
            upd_has_mssat.save()
            messages.success(request, "SUCCESSFULLY ADDED")
            redirect_url_with_args = f'/{uis}/{misc_uis}/new_mssat_pdf'
            return redirect(redirect_url_with_args)  
        return render(request, 'uis/new_add_mss_tool.html',{'uis_misc':misc_uis,'time_start':request.session['mssat_start'],'time_endede':time_endede,'uis_g':uis_g,'info_g':info_g,'mms_no_auto':mms_no_auto,'date_today':date_today,'uis':uis,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")
    
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
            messages.success(request, "SUCCESSFULLY UPDATED")
            redirect_url_with_args = f'/{mssat}/update_msstool'
            return redirect(redirect_url_with_args)
    else:
        return HttpResponseRedirect("/auth_login")
    

