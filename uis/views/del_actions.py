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
def del_famcom(request, uis_id,famcom_id,uis_misc):
    try:
        FamilyComposition.objects.filter(familyComposition=famcom_id).delete()
        messages.success(request, 'Sucessfully Deleted!')
    except RestrictedError:
        messages.warning(request, 'Cannot Delete this Data!')
    redirect_url_with_args = f'/{uis_id}/{uis_misc}/update_uis'
    return redirect(redirect_url_with_args)
def delete_scp_tab(request, scp_tab_id, mssat):
    try:
        scp_table.objects.filter(scp_table=scp_tab_id).delete()
        messages.success(request, 'Sucessfully Deleted!')
    except RestrictedError:
        messages.warning(request, 'Cannot Delete this Data!')
    redirect_url_with_args = f'/{mssat}/edit_scp'
    return redirect(redirect_url_with_args)

def del_reccom(request, uis_id,reccom_id,uis_misc):
    try:
        reccom_del_amt = Recommendations.objects.get(recommendation = reccom_id)
        asst_del_amt = float(reccom_del_amt.amt_of_assistance)
        misc_uis =UIS_misc.objects.get(uis_misc=uis_misc)
        init_amt = float(misc_uis.total_amount_of_assistance) 
        misc_uis.total_amount_of_assistance = init_amt - asst_del_amt
        misc_uis.save()
        Recommendations.objects.filter(recommendation=reccom_id).delete()
        messages.success(request, 'Sucessfully Deleted!')
    except RestrictedError:
        messages.warning(request, 'Cannot Delete this Data!')
    redirect_url_with_args = f'/{uis_id}/{uis_misc}/edit_uis'
    return redirect(redirect_url_with_args)

def del_famcom_osof(request, uis_id,osof_id,uis_misc):
    try:
        Fc_other_source.objects.filter(fc_other_source=osof_id).delete()
        messages.success(request, 'Sucessfully Deleted!')
    except RestrictedError:
        messages.warning(request, 'Cannot Delete this Data!')
    redirect_url_with_args = f'/{uis_id}/{uis_misc}/update_uis'
    return redirect(redirect_url_with_args)

