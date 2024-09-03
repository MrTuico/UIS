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

def social_profile(request):
    query = request.GET.get('search', '')
    if query:
        uis_show = UIS.objects.all()
       
        show = IdentifyingInformation.objects.filter(Q (client_name__icontains=query))
    else:
        uis_show = UIS.objects.all()
      
        show = IdentifyingInformation.objects.all()[:10]
    return render(request,'uis/scsr_list.html',{'show':show,'uis':uis_show,'user':request.session['name']})