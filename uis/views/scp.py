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

def get_patient_scp_history(request,uis,uis_miscs,mssats):
    if request.session.get('employee_id') is not None:
        try:
            iden = IdentifyingInformation.objects.get(uis=uis)
            fullname = iden.client_name
            hospno = iden.uis.hospno
            uis_misc = UIS_misc.objects.filter(uis=uis,has_mssat=1)
            informant = Informant.objects.filter(uis=uis)
            mssat = MSSAT.objects.filter(uis=uis)
            scp = SCP.objects.filter(mssat=mssats)
            return render(request, 'uis/scp_history.html',{'uis_miscs':uis_miscs,'mssats':mssats,'scp':scp,'uis':uis,'uis_misc':uis_misc,'mssat':mssat,'fullname':fullname,'hospno':hospno,'informant':informant,'user':request.session['name']})
        except ObjectDoesNotExist:
            return render(request, 'uis/scp_history.html',{'uis_miscs':uis_miscs,'mssats':mssats,'scp':scp,'uis_misc':uis_misc,'informant':informant,'mssat':mssat,'fullname':fullname,'hospno':hospno,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")
    
def add_scp(request,uis,uis_miscs,mssats):
    if request.session.get('employee_id') is not None:
        if request.method == 'POST':
            pa = request.POST.get('pa')
            eligible = request.POST.get('eligible',False)
            oth = request.POST.get('oth',False)
            if eligible:
                rfom = "ELIGIBLE"
            elif oth:
                rfom = request.POST.get('others')
            uis_id = UIS.objects.get(uis = uis) 
            uis_misc_id = UIS_misc.objects.get(uis_misc = uis_miscs)
            mssat_id = MSSAT.objects.get(mssat = mssats)
            a = SCP(uis = uis_id,uis_misc=uis_misc_id,mssat=mssat_id,psychosocial_assessment= pa,reccomendation_for_oth_member=rfom)
            a.save()
            if a.scp:
                scp = SCP.objects.get(scp = a.scp)
                scpdata = request.POST.get('scpdata')
                if scpdata:
                    reccom_data = json.loads(scpdata)
                    for r in reccom_data:
                        area = r['area']
                        pn = r['pn']
                        go = r['go']
                        ti = r['ti']
                        fd = r['fd']
                        rp = r['rp']
                        eo = r['eo']
                        b = scp_table(scp=scp,area= area,problem_need=pn,goals_objective=go,treatment_intervention=ti,frequency_duration=fd,responsible_person=rp,expected_output=eo)
                        b.save()
                    else:
                        reccom_data = []
            redirect_url_with_args = f'/{uis_id}/{uis_miscs}/{mssats}/psycoProfile'
            messages.success(request, "SUCCESSFULLY ADDED")
            return redirect(redirect_url_with_args)

        return render(request, 'uis/add_scp.html',{'mssats':mssats,'uis':uis,'uis_miscs':uis_miscs,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")
def edit_scp(request,mssat):
    if request.session.get('employee_id') is not None:
        get_scp = SCP.objects.get(mssat=mssat)
        get_scp_tab = scp_table.objects.filter(scp=get_scp.scp)
        return render(request, 'uis/edit_scp.html',{'scp_tab':get_scp_tab,'scp':get_scp,'mssat':mssat,'user':request.session['name']})
    else:
        return HttpResponseRedirect("/auth_login")
def process_edit_scp(request,scp, mssat):
    if request.session.get('employee_id') is not None:
        try:
            if request.method == 'POST':
                pa = request.POST.get('pa')
                eligible = request.POST.get('eligible',False)
                oth = request.POST.get('oth',False)
                if eligible:
                    rfom = "ELIGIBLE"
                elif oth:
                    rfom = request.POST.get('others')
        except(KeyError):
            return render(request, 'uis/edit_scp.html',{
                'error_message':"PROBLEM IN UPDATING",
                })
        else:
            scp_ups = SCP.objects.get(scp=scp)
            scp_ups.psychosocial_assessment = pa
            scp_ups.reccomendation_for_oth_member = rfom
            scp_ups.save()
            scp_id = SCP.objects.get(scp = scp)
            scpdata = request.POST.get('scpdata')
            if scpdata:
                reccom_data = json.loads(scpdata)
                for r in reccom_data:
                    area = r['area']
                    pn = r['pn']
                    go = r['go']
                    ti = r['ti']
                    fd = r['fd']
                    rp = r['rp']
                    eo = r['eo']
                    b = scp_table(scp=scp_id,area= area,problem_need=pn,goals_objective=go,treatment_intervention=ti,frequency_duration=fd,responsible_person=rp,expected_output=eo)
                    b.save()
                else:
                    reccom_data = []
            redirect_url_with_args = f'/{mssat}/edit_scp'
            messages.success(request, "SUCCESSFULLY UPDATED")
            return redirect(redirect_url_with_args)  
    else:
        return HttpResponseRedirect("/auth_login")
    
