from django.shortcuts import render,get_object_or_404,reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, FileResponse
from django.core.exceptions import ObjectDoesNotExist
from reportlab.pdfgen import canvas
import io
from reportlab.lib.colors import blue, gray, whitesmoke,white,black,skyblue
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from datetime import date, datetime, time
from uis.models import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

def create_header(c,doc):
    logo = 'uis/static/logo.png'
    doh_logo = 'uis/static/doh.png'
    c.saveState()
    c.drawImage(logo, 1.28*inch, 10.69*inch, mask='auto', width=70, height=70)
    c.drawImage(doh_logo, 0.27*inch, 10.69*inch, mask='auto', width=70, height=70)
    c.setFont("Times-Roman", 12, leading=None)
    c.setFillColor("green")
    c.drawString(2.3*inch, 11.49*inch, "Bicol Region General Hospital and Geriatric Medical Center")
    c.drawString(3.1*inch, 11.29*inch, "(Formely BICOL SANITARIUM)")
    c.setFont("Times-Roman", 11, leading=None)
    c.setFillColor("black")
    c.drawString(3.2*inch, 11.14*inch, "San Pedro, Cabusao Camarines Sur")
    c.drawString(2.4*inch, 10.99*inch, "Telephone Nos.: (054) 473-2244, 472-4422, 881-1033, 881-1761")
    c.drawString(2.5*inch, 10.85*inch, "E-mail Address: bicolsan@gmail.com, brghgmc@gmail.com")
    # c.setStrokeColorRGB(0, 0, 1)  # Blue color
    # c.setLineWidth(2)
    # c.line(0.25*inch,10.55*inch,8*inch,10.55*inch)
    c.restoreState()
def create_footer(c,doc):
    padaba = 'uis/static/padabrghgmc.png'
    c.setStrokeColorRGB(0, 0, 1)  # Blue color
    c.line(0, 0.4*inch, 800, 0.4*inch) #(x1, y1, x2, y2)
    c.setFont("Times-Italic", 10, leading=None)
    c.drawString(0.77*inch, 0.20*inch, "BRGHGMC-F-HOPSS-EFM-003")
    c.drawString(3.2*inch, 0.20*inch, "Rev 2")
    c.drawString(4.7*inch, 0.20*inch, "Effectivity Date: May 2, 2023")
    c.drawImage(padaba, 6.6*inch, 0.06*inch, mask='auto', width=100, height=20)

def new_mssat_pdf(request,uis):
    
    page1 = 1
    page2 = 2
    page3 = 3
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    custom_font_size_swa = style.clone('CustomStyle')
    custom_font_size_swa_first = style.clone('CustomStyle')
    custom_font_size_swa.fontSize = 6.5
    custom_font_size_swa.leading = 6.5
    custom_font_size_swa_first.fontSize = 3.5
    custom_font_size_swa_first.leading = 3.5
    if page1 == 1:
        buf = io.BytesIO()
        c = canvas.Canvas(buf)
        response = HttpResponse(content_type='application/pdf')
        c.setTitle("MSWD ASSESSMENT TOOL")
        c.setPageSize((8.27*inch, 11.69*inch))
        # c.setLineWidth(2)
        # c.setStrokeColor(skyblue)
        # c.line(0.25*inch,10.55*inch,8*inch,10.55*inch)
    
        # ---------box--------
        c.setStrokeColor(black)
        c.setLineWidth(1)# horizontalline top
        c.line(0.25*inch,10.45*inch,8*inch,10.45*inch)

        c.setLineWidth(1)# horizontalline bottom
        c.line(0.25*inch,0.55*inch,8*inch,0.55*inch)

        c.setLineWidth(1)# verticalline left
        c.line(0.25*inch,0.55*inch,0.25*inch,10.45*inch)

        c.setLineWidth(1)# verticalline right
        c.line(8*inch,0.55*inch,8*inch,10.45*inch)

        # ---------end box--------
        styles = getSampleStyleSheet()
        style = styles["Normal"]
        custom_font_size = style.clone('CustomStyle')
        custom_font_size.fontSize = 7
        custom_font_size.leading = 7

        c.setFillColor("black")
        c.setFont("Times-Bold", 13, leading=None)
        c.drawString(0.7*inch, 10.54*inch, "MEDICAL SOCIAL WORK DEPARTMENT ASSESSMENT TOOL")
        c.setFillColor("black")
        c.setFont("Times-Bold", 6, leading=None)
        c.drawString(6.6*inch, 10.66*inch, "     Form Code:     FM-ANC-MSS-01")
        c.drawString(6.6*inch, 10.57*inch, "      Effectivity:     September 13, 2023")
        c.drawString(6.6*inch, 10.48*inch, "         Revision:     1")

        c.setFillColor(white)#Date of Interview
        c.rect(0.25*inch,10.3*inch,7.75*inch,0.15*inch,fill=1)
        c.rect(1.25*inch,10.3*inch,1*inch,0.15*inch,fill=1)# input field
        c.rect(3.25*inch,10.3*inch,1*inch,0.15*inch,fill=1)# input field2
        

        c.setFillColor(whitesmoke)#Date of Interview
        c.rect(0.25*inch,10.3*inch,1*inch,0.15*inch,fill=1)
        c.rect(2.25*inch,10.3*inch,1*inch,0.15*inch,fill=1)
        c.rect(4.25*inch,10.3*inch,3.75*inch,0.15*inch,fill=1)


        c.setFillColor(white)# Time of Interview
        c.rect(0.25*inch,10.15*inch,7.75*inch,0.15*inch,fill=1)
        c.rect(1.25*inch,10.15*inch,1*inch,0.15*inch,fill=1)# input field
        c.rect(3.25*inch,10.15*inch,1*inch,0.15*inch,fill=1)# input field2

        c.rect(4.3*inch,10.17*inch,0.09*inch,0.09*inch,fill=1)#box in-patient
        c.rect(5.1*inch,10.17*inch,0.09*inch,0.09*inch,fill=1)#box Out-Patient
        c.rect(6*inch,10.17*inch,0.09*inch,0.09*inch,fill=1)#box Walkin
        c.rect(6.8*inch,10.17*inch,0.09*inch,0.09*inch,fill=1)#box ER SURG
        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(4.5*inch, 10.17*inch, "In-Patient")
        c.drawString(5.3*inch, 10.17*inch, "Out-Patient")
        c.drawString(6.2*inch, 10.17*inch, "Walk-In")
        c.drawString(7*inch, 10.17*inch, "ER SURG")

        c.setFillColor(whitesmoke)# Time of Interview
        c.rect(0.25*inch,10.15*inch,1*inch,0.15*inch,fill=1)
        c.rect(2.25*inch,10.15*inch,1*inch,0.15*inch,fill=1)

        c.setFillColor(white)#venue of interview
        c.rect(0.25*inch,10*inch,7.75*inch,0.15*inch,fill=1)
        c.rect(1.25*inch,10*inch,1*inch,0.15*inch,fill=1)# input field
        c.rect(3.25*inch,10*inch,1*inch,0.15*inch,fill=1)# input field2
        
        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(4.5*inch, 10.02*inch, "Old Case")
        c.drawString(5.3*inch, 10.02*inch, "New Case")
        c.drawString(6.2*inch, 10.02*inch, "Forwarded")
        c.drawString(7*inch, 10.02*inch, "Closed")

        c.setFillColor(whitesmoke)#venue of interview
        c.rect(0.25*inch,10*inch,1*inch,0.15*inch,fill=1)
        c.rect(2.25*inch,10*inch,1*inch,0.15*inch,fill=1)

        c.setFillColor(white)#end of interview
        c.rect(0.25*inch,9.85*inch,7.75*inch,0.15*inch,fill=1)
        c.rect(1.25*inch,9.85*inch,1*inch,0.15*inch,fill=1)# input field
        c.rect(3.25*inch,9.85*inch,1*inch,0.15*inch,fill=1)# input field2
        
        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(4.5*inch, 9.87*inch, "Service")
        c.drawString(5.3*inch, 9.87*inch, "Semi-Private")
        c.drawString(6.2*inch, 9.87*inch, "Private")

        c.setFillColor(whitesmoke)#end of interview
        c.rect(0.25*inch,9.85*inch,1*inch,0.15*inch,fill=1)
        c.rect(2.25*inch,9.85*inch,1*inch,0.15*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.28*inch, 10.32*inch, "Date of Interview:")
        c.drawString(0.28*inch, 10.17*inch, "Start of Interview(Time):")
        c.drawString(0.28*inch, 10.02*inch, "Venue of Interview:")
        c.drawString(0.28*inch, 9.87*inch, "End of Interview(Time):")
        c.drawString(4.28*inch, 10.32*inch, "CATEGORY: (please shade)")
        c.drawString(2.26*inch, 10.32*inch, "Date admitted/consulted:")
        c.drawString(2.28*inch, 10.17*inch, "Hospital Number:")
        
        c.drawString(2.28*inch, 10.02*inch, "MSS Number:")
        c.drawString(2.28*inch, 9.87*inch, "PHIC ID Number:")

        c.setFillColor(white)#blank space
        c.rect(0.25*inch,9.7*inch,7.75*inch,0.15*inch,fill=1)
        
        c.setFillColor(skyblue)#single
        c.rect(0.25*inch,9.55*inch,7.75*inch,0.15*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.28*inch, 9.58*inch, "SOURCE OF REFERRAL")
        
        get_details = UIS.objects.filter(uis = uis)
        for i in get_details:
            hospno = i.hospno
            hsize_f = float(i.householdsize)
            hsize = i.householdsize
            philnum = i.phil_no
            tot_income_f = float(i.total_income)
            tot_income = i.total_income
            tot_expense = float(i.total_expense)
            per_capita_income = tot_income_f/hsize_f
            mswd_cat = i.category
            c.setFillColor("black")
            c.setFont("Times-Bold", 9, leading=None)
            c.drawString(3.3*inch, 10.17*inch, hospno)
            c.drawString(3.3*inch, 9.87*inch, philnum)
        informant_details = Informant.objects.filter(uis = uis)
        for a in informant_details:
            doi_init = a.date_of_intake
            date_conv = datetime.strptime(doi_init, '%Y-%m-%d')
            doi = date_conv.strftime('%B %d, %Y')
            informant_fullname = a.fullname
            informant_address = a.address
            informant_time_of_interview = a.time_of_interview
            informant_end_time_of_interview = a.end_time_of_interview
            informant_relation_to_patient = a.relation_to_patient
            informant_contact_number = a.contact_number
            c.setFillColor("black")
            c.setFont("Times-Bold", 9, leading=None)
            c.drawString(1.3*inch, 10.32*inch, doi)
            c.drawString(1.3*inch, 10.17*inch, informant_time_of_interview)
            c.drawString(1.3*inch, 9.87*inch,  informant_end_time_of_interview)
            c.drawString(0.4*inch, 9.1*inch, informant_fullname)
        mssat = MSSAT.objects.filter(uis = uis)
        for sc in mssat:
            fuel_src_init = sc.fuel_source
            conv_fuel_src = fuel_src_init.replace("[","").replace("]","").replace("'","")
            f_fsrc = conv_fuel_src.replace(" ","")
            fuel_src = f_fsrc.split(',')
            amt_fuel_src_init = sc.amt_fuel_source
            conv_amt_fsrc = amt_fuel_src_init.replace("[","").replace("]","").replace("'","")
            amt_fuel_src = conv_amt_fsrc.split(',')
            clothing_amt = sc.clothing_amt
            tla = sc.tla
            sc_category = sc.category
            phil_mem = sc.phil_mem
            mswd = sc.mswd_cassif
            employer = sc.employer
            venue = sc.venue
            ward = sc.basic_ward
            doac_init = sc.doac
            date_conv = datetime.strptime(doac_init, '%Y-%m-%d')
            doac = date_conv.strftime('%B %d, %Y')
            duration_of_prob = sc.duration_of_prob
            marginalized_sec_mem = sc.marginalized_sec_mem
            prev_treatment = sc.prev_treatment
            health_accessibility_prob = sc.health_accessibility_prob
            src_referal_name = sc.src_referal_name
            src_address = sc.address
            src_cnum  = sc.cnum 
            c.setFillColor("black")
            c.setFont("Times-Bold", 9, leading=None)
            c.drawString(3.3*inch, 10.32*inch, doac)
            c.drawString(3.3*inch, 10.02*inch, sc.mss_no)
            c.drawString(6.55*inch, 9.87*inch, "Ward:")
            c.setFillColor("red")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(7.65*inch, 10.17*inch, mswd_cat)
            c.drawString(6.9*inch, 9.87*inch,  ward)
            c.setFillColor("black")
            c.setFont("Times-Bold", 5.5, leading=None)
            c.drawString(1.28*inch, 10.04*inch, venue)
            
            if sc_category == 'IN-PATIENT':
                c.setFillColor(black)
                c.rect(4.3*inch,10.17*inch,0.09*inch,0.09*inch,fill=1)#box in-patient
            else:
                c.setFillColor(white)
                c.rect(4.3*inch,10.17*inch,0.09*inch,0.09*inch,fill=1)#box in-patient
            if sc_category == 'OUT-PATIENT':
                c.setFillColor(black)
                c.rect(5.1*inch,10.17*inch,0.09*inch,0.09*inch,fill=1)#box Out-Patient
            else:
                c.setFillColor(white)
                c.rect(5.1*inch,10.17*inch,0.09*inch,0.09*inch,fill=1)#box Out-Patient
            if sc_category == 'WALK-IN':
                c.setFillColor(black)
                c.rect(6*inch,10.17*inch,0.09*inch,0.09*inch,fill=1)#box Walkin
            else:
                c.setFillColor(white)
                c.rect(6*inch,10.17*inch,0.09*inch,0.09*inch,fill=1)#box Walkin
            if sc_category == 'ER SURG':
                c.setFillColor(black)
                c.rect(6.8*inch,10.17*inch,0.09*inch,0.09*inch,fill=1)#box ER SURG
            else:
                c.setFillColor(white)
                c.rect(6.8*inch,10.17*inch,0.09*inch,0.09*inch,fill=1)#box ER SURG
            if sc_category == 'OLD CASE':
                c.setFillColor(black)
                c.rect(4.3*inch,10.02*inch,0.09*inch,0.09*inch,fill=1)#box old-case
            else:
                c.setFillColor(white)
                c.rect(4.3*inch,10.02*inch,0.09*inch,0.09*inch,fill=1)#box old-case
            if sc_category == 'NEW CASE':
                c.setFillColor(black)
                c.rect(5.1*inch,10.02*inch,0.09*inch,0.09*inch,fill=1)#box New case
            else:
                c.setFillColor(white)
                c.rect(5.1*inch,10.02*inch,0.09*inch,0.09*inch,fill=1)#box New case
            if sc_category == 'FORWARDED':
                c.setFillColor(black)
                c.rect(6*inch,10.02*inch,0.09*inch,0.09*inch,fill=1)#box Forwarded
            else:
                c.setFillColor(white)
                c.rect(6*inch,10.02*inch,0.09*inch,0.09*inch,fill=1)#box Forwarded
            if sc_category == 'CLOSED':
                c.setFillColor(black)
                c.rect(6.8*inch,10.02*inch,0.09*inch,0.09*inch,fill=1)#box closed
            else:
                c.setFillColor(white)
                c.rect(6.8*inch,10.02*inch,0.09*inch,0.09*inch,fill=1)#box closed
            if sc_category == 'SERVICE':
                c.setFillColor(black)
                c.rect(4.3*inch,9.87*inch,0.09*inch,0.09*inch,fill=1)#box Service
            else:
                c.setFillColor(white)
                c.rect(4.3*inch,9.87*inch,0.09*inch,0.09*inch,fill=1)#box Service
            if sc_category == 'SEMI-PRIVATE':
                c.setFillColor(black)
                c.rect(5.1*inch,9.87*inch,0.09*inch,0.09*inch,fill=1)#box Semi-Private
            else:
                c.setFillColor(white)
                c.rect(5.1*inch,9.87*inch,0.09*inch,0.09*inch,fill=1)#box Semi-Private
            if sc_category == 'PRIVATE':
                c.setFillColor(black)
                c.rect(6*inch,9.87*inch,0.09*inch,0.09*inch,fill=1)#box PRIVATE
            else:
                c.setFillColor(white)
                c.rect(6*inch,9.87*inch,0.09*inch,0.09*inch,fill=1)#box PRIVATE

        c.setFillColor(white)#source of referal
        c.rect(0.25*inch,9.3*inch,2*inch,0.25*inch,fill=1)
        c.rect(2.25*inch,9.3*inch,3*inch,0.25*inch,fill=1)
        c.rect(5.25*inch,9.3*inch,2.75*inch,0.25*inch,fill=1)

        c.setFillColor(whitesmoke)#source of referal
        c.rect(0.25*inch,9.45*inch,7.75*inch,0.1*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.3*inch, 9.34*inch, src_referal_name)
        c.drawString(2.3*inch, 9.34*inch, src_address)
        c.drawString(5.3*inch, 9.34*inch, src_cnum)

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.28*inch, 9.46*inch, "Name:")
        c.drawString(2.28*inch, 9.46*inch, "Address:")
        c.drawString(5.28*inch, 9.46*inch, "Contact Number:")

        c.setFillColor(white)#Informant
        c.rect(0.25*inch,9*inch,2*inch,0.3*inch,fill=1)
        c.rect(2.25*inch,9*inch,2*inch,0.3*inch,fill=1)
        c.rect(4.25*inch,9*inch,1*inch,0.3*inch,fill=1)
        c.rect(5.25*inch,9*inch,2.75*inch,0.3*inch,fill=1)

        c.setFillColor(whitesmoke)#source of referal
        c.rect(0.25*inch,9.2*inch,7.75*inch,0.1*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.28*inch, 9.21*inch, "Informant:")
        c.drawString(2.28*inch, 9.21*inch, "Relation to patient")
        c.drawString(4.3*inch, 9.21*inch, "Contact Number")
        c.drawString(5.28*inch, 9.21*inch, "Address of Informant:")

        c.setFillColor("black")
        c.setFont("Times-Bold", 6.5, leading=None)
        c.drawString(0.3*inch, 9.1*inch, informant_fullname)
        c.drawString(2.3*inch, 9.1*inch, informant_relation_to_patient)
        c.drawString(4.3*inch, 9.1*inch, informant_contact_number)
        c.drawString(5.3*inch, 9.1*inch, informant_address)

        c.setFillColor(skyblue)#4
        c.rect(0.25*inch,8.9*inch,7.75*inch,0.15*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.28*inch, 8.95*inch, "DEMOPGRAPHIC DATA:")

        c.setFillColor(whitesmoke)#patient name
        c.rect(0.25*inch,8.6*inch,1*inch,0.3*inch,fill=1)
        c.rect(1.25*inch,8.77*inch,6.75*inch,0.13*inch,fill=1)
        c.setFillColor(white)#patient name input field
        c.rect(1.25*inch,8.6*inch,6.75*inch,0.17*inch,fill=1)
        
        indentyInfo = IdentifyingInformation.objects.filter(uis = uis)
        for b in indentyInfo:
            dob_init = b.dob
            date_dob = datetime.strptime(dob_init, '%Y-%m-%d')
            ii_dob = date_dob.strftime('%B %d, %Y')
            ii_cname = b.client_name
            ii_gender = b.gender
            ii_age = b.age
            ii_pob = b.pob
            ii_pra = b.present_address
            ii_perma = b.permanent_address
            ii_cstat = b.cstat
            ii_rel = b.religion
            ii_hea = b.hea
            ii_nat = b.nationality
            ii_occu = b.occupation
            ii_mi_init = b.mi
            ii_mi = '{:,.2f}'.format(float(ii_mi_init))
            ii_pt = b.patient_type

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 8.7*inch, "Patient's Name")
        c.drawString(1.35*inch, 8.8*inch, "Surname")
        c.drawString(3.3*inch, 8.8*inch, "First Name")
        c.drawString(5.3*inch, 8.8*inch, "Last Name")
        c.drawString(7.2*inch, 8.8*inch, "Ext.(Sr., Jr.)")
            
        c.setFillColor(whitesmoke)
        c.rect(0.25*inch,8.45*inch,1*inch,0.15*inch,fill=1)#date of birth
        c.rect(0.25*inch,8.3*inch,1*inch,0.15*inch,fill=1)#contact no.
        c.rect(0.25*inch,8.15*inch,1*inch,0.15*inch,fill=1)#relegion
        c.rect(0.25*inch,8*inch,1*inch,0.15*inch,fill=1)#permanent address
        c.rect(2.25*inch,8.45*inch,1*inch,0.15*inch,fill=1)#age
        c.rect(2.25*inch,8.3*inch,1*inch,0.15*inch,fill=1)#place of birth
        c.rect(5.25*inch,8.45*inch,1*inch,0.15*inch,fill=1)#Sex
        c.rect(5.25*inch,8.3*inch,1*inch,0.15*inch,fill=1)#Gender
        c.rect(5.25*inch,8.15*inch,1*inch,0.15*inch,fill=1)#nationality
        c.rect(5.25*inch,8*inch,1*inch,0.15*inch,fill=1)#temp address
        c.rect(0.25*inch,7.7*inch,1*inch,0.3*inch,fill=1)#civil status
        c.rect(5.25*inch,7.7*inch,1*inch,0.3*inch,fill=1)#Type of living arrangement
        c.rect(5.25*inch,7.55*inch,1*inch,0.15*inch,fill=1)#OCCUPATION
        c.rect(5.25*inch,7.4*inch,1*inch,0.15*inch,fill=1)#Patient m.i
        c.rect(5.25*inch,7.1*inch,1*inch,0.3*inch,fill=1)#Philhealth Membership number(pin)
        c.rect(0.25*inch,7.1*inch,1*inch,0.6*inch,fill=1)#HEA
        
        c.setFillColor(white)
        c.rect(1.25*inch,8.45*inch,1*inch,0.15*inch,fill=1)#date of birth
        c.rect(1.25*inch,8.3*inch,1*inch,0.15*inch,fill=1)#contact no.
        c.rect(3.25*inch,8.45*inch,2*inch,0.15*inch,fill=1)#age
        c.rect(3.25*inch,8.3*inch,2*inch,0.15*inch,fill=1)#place of birth
        c.rect(6.25*inch,8.45*inch,1.75*inch,0.15*inch,fill=1)#Sex
        c.rect(6.25*inch,8.3*inch,1.75*inch,0.15*inch,fill=1)#Gender
        c.rect(1.25*inch,8.15*inch,4*inch,0.15*inch,fill=1)#religion
        c.rect(1.25*inch,8*inch,4*inch,0.15*inch,fill=1)#permanent address
        c.rect(6.25*inch,8.15*inch,1.75*inch,0.15*inch,fill=1)#nationality
        c.rect(6.25*inch,8*inch,1.75*inch,0.15*inch,fill=1)#temp address
        c.rect(1.25*inch,7.7*inch,4*inch,0.3*inch,fill=1)#civil status
        c.rect(6.25*inch,7.55*inch,1.75*inch,0.15*inch,fill=1)#occupation
        c.rect(6.25*inch,7.4*inch,1.75*inch,0.15*inch,fill=1)#patient m.i
        c.rect(6.25*inch,7.7*inch,1.75*inch,0.3*inch,fill=1)#type of living arrangement
        c.rect(1.25*inch,7.1*inch,4*inch,0.6*inch,fill=1)#hea
        c.rect(6.25*inch,7.1*inch,1.75*inch,0.3*inch,fill=1)#Philhealth Membership number(pin)

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(1.3*inch, 8.63*inch, ii_cname)
        c.drawString(1.3*inch, 8.48*inch, ii_dob)
        c.drawString(3.3*inch, 8.48*inch, ii_age)
        c.drawString(6.3*inch, 8.48*inch, ii_gender)
        c.drawString(1.3*inch, 8.33*inch, informant_contact_number)
        c.drawString(3.3*inch, 8.33*inch, ii_pob)
        c.drawString(6.3*inch, 8.33*inch, ii_gender)
        c.drawString(1.3*inch, 8.18*inch, ii_rel)
        c.drawString(1.3*inch, 8.03*inch, ii_perma)
        c.drawString(6.3*inch, 8.18*inch, ii_nat)
        c.drawString(6.3*inch, 7.75*inch, tla)
        c.drawString(6.3*inch, 7.58*inch, ii_occu)
        c.drawString(6.3*inch, 7.43*inch, ii_mi)
        c.setFont("Times-Bold", 5, leading=None)
        c.drawString(6.3*inch, 8.03*inch, ii_pra)
       
        


        if ii_cstat == 'SINGLE':
            c.setFillColor(black)#box civil status
            c.rect(1.3*inch,7.88*inch,0.09*inch,0.09*inch,fill=1)#single
        else:
            c.setFillColor(white)#box civil status
            c.rect(1.3*inch,7.88*inch,0.09*inch,0.09*inch,fill=1)#single
        if ii_cstat == 'MARRIED':
            c.setFillColor(black)#box civil status
            c.rect(2.3*inch,7.88*inch,0.09*inch,0.09*inch,fill=1)#married
        else:
            c.setFillColor(white)#box civil status
            c.rect(2.3*inch,7.88*inch,0.09*inch,0.09*inch,fill=1)#married
        if ii_cstat == 'COMMON-LAW':
            c.setFillColor(black)#box civil status
            c.rect(3.3*inch,7.88*inch,0.09*inch,0.09*inch,fill=1)#common-law
        else:
            c.setFillColor(white)#box civil status
            c.rect(3.3*inch,7.88*inch,0.09*inch,0.09*inch,fill=1)#common-law
        if ii_cstat == 'WIDOWED':
            c.setFillColor(black)#box civil status
            c.rect(4.3*inch,7.88*inch,0.09*inch,0.09*inch,fill=1)#widowed
        else:
            c.setFillColor(white)#box civil status
            c.rect(4.3*inch,7.88*inch,0.09*inch,0.09*inch,fill=1)#widowed
        if ii_cstat == 'SEPARATED':
            c.setFillColor(black)#box civil status
            c.rect(1.3*inch,7.74*inch,0.09*inch,0.09*inch,fill=1)#separated
        else:
            c.setFillColor(white)#box civil status
            c.rect(1.3*inch,7.74*inch,0.09*inch,0.09*inch,fill=1)#separated
        if ii_cstat == 'LEGALLY':
            c.setFillColor(black)#box civil status
            c.rect(2.3*inch,7.74*inch,0.09*inch,0.09*inch,fill=1)#legally
        else:
            c.setFillColor(white)#box civil status
            c.rect(2.3*inch,7.74*inch,0.09*inch,0.09*inch,fill=1)#legally
        if ii_cstat == 'IN FACT':
            c.setFillColor(black)#box civil status
            c.rect(3.3*inch,7.74*inch,0.09*inch,0.09*inch,fill=1)#in Fact
        else:
            c.setFillColor(white)#box civil status
            c.rect(3.3*inch,7.74*inch,0.09*inch,0.09*inch,fill=1)#in Fact

       

        c.setFillColor("black")# naming con. civil status
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(1.42*inch, 7.88*inch, "Single")
        c.drawString(2.42*inch, 7.88*inch, "Married")
        c.drawString(3.42*inch, 7.88*inch, "Common-Law")
        c.drawString(4.42*inch, 7.88*inch, "Widowed")
        c.drawString(1.42*inch, 7.74*inch, "Separated")
        c.drawString(2.42*inch, 7.74*inch, "Legally")
        c.drawString(3.42*inch, 7.74*inch, "In Fact")


        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 8.48*inch, "Date of Birth:")
        c.drawString(0.3*inch, 8.33*inch, "Contact No.:")
        c.drawString(0.3*inch, 8.18*inch, "Religion:")
        c.drawString(0.3*inch, 8.03*inch, "Permanent Address:")
        c.drawString(0.3*inch, 7.8*inch, "Civil Status(shade):")
        c.drawString(0.3*inch, 7.45*inch, "Highest Educational")
        c.drawString(0.3*inch, 7.35*inch, "Attainment")
        c.drawString(2.27*inch, 8.48*inch, "Age:")
        c.drawString(2.27*inch, 8.33*inch, "Place of Birth:")
        c.drawString(5.27*inch, 8.48*inch, "Sex:")
        c.drawString(5.27*inch, 8.33*inch, "Gender:")
        c.drawString(5.27*inch, 8.18*inch, "Nationality:")
        c.drawString(5.27*inch, 8.03*inch, "Tempory Address:")
        c.drawString(5.27*inch, 7.85*inch, "Type of Living")
        c.drawString(5.27*inch, 7.75*inch, "Arrangement")
        c.drawString(5.27*inch, 7.57*inch, "Occupation")
        c.drawString(5.27*inch, 7.42*inch, "Pat. Monthly Income")
        c.drawString(5.27*inch, 7.28*inch, "Philhealth")
        c.drawString(5.27*inch, 7.18*inch, "Membership no.(PIN)")

        if ii_hea =='ELEMENTARY':
            c.setFillColor(black)#box hea
            c.rect(1.3*inch,7.55*inch,0.09*inch,0.09*inch,fill=1)#Primary
        else:
            c.setFillColor(white)#box hea
            c.rect(1.3*inch,7.55*inch,0.09*inch,0.09*inch,fill=1)#Primary
        if ii_hea =='HIGH SCHOOL':
            c.setFillColor(black)#box hea
            c.rect(2.3*inch,7.55*inch,0.09*inch,0.09*inch,fill=1)#Secondary
        else:
            c.setFillColor(white)#box hea
            c.rect(2.3*inch,7.55*inch,0.09*inch,0.09*inch,fill=1)#Secondary
        if ii_hea =='VOCATIONAL':
            c.setFillColor(black)#box hea
            c.rect(3.3*inch,7.55*inch,0.09*inch,0.09*inch,fill=1)#Vocational
        else:
            c.setFillColor(white)#box hea
            c.rect(3.3*inch,7.55*inch,0.09*inch,0.09*inch,fill=1)#Vocational
        if ii_hea =='COLLEGE':
            c.setFillColor(black)#box hea
            c.rect(1.3*inch,7.4*inch,0.09*inch,0.09*inch,fill=1)#Tertiary
        else:
            c.setFillColor(white)#box hea
            c.rect(1.3*inch,7.4*inch,0.09*inch,0.09*inch,fill=1)#Tertiary
        if ii_hea =='':
            c.rect(2.3*inch,7.4*inch,0.09*inch,0.09*inch,fill=1)#legally
        if ii_hea =='NONE':
            c.setFillColor(black)#box hea
            c.rect(1.3*inch,7.25*inch,0.09*inch,0.09*inch,fill=1)#No educational attainment
        else:
            c.setFillColor(white)#box hea
            c.rect(1.3*inch,7.25*inch,0.09*inch,0.09*inch,fill=1)#No educational attainment
        if ii_hea =='POST-GRADUATE':
            c.setFillColor(black)#box hea
            c.rect(2.3*inch,7.4*inch,0.09*inch,0.09*inch,fill=1)#No educational attainment
        else:
            c.setFillColor(white)#box hea
            c.rect(2.3*inch,7.4*inch,0.09*inch,0.09*inch,fill=1)#No educational attainment
        
    
        c.setFillColor("black")# naming con. hea
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(2.42*inch, 7.4*inch, "Post Graduate")
        c.drawString(1.42*inch, 7.4*inch, "Tertiary")
        c.drawString(1.42*inch, 7.25*inch, "No Educational Attainment")
        c.drawString(1.42*inch, 7.55*inch, "Primary")
        c.drawString(2.42*inch, 7.55*inch, "Secondary")
        c.drawString(3.42*inch, 7.55*inch, "Vocational")

        if phil_mem == 'DIRECT CONTRIBUTOR':
            c.setFillColor(black)#phil membeship
            c.rect(6.3*inch,7.27*inch,0.09*inch,0.09*inch,fill=1)#Direct Contributor
        else:
            c.setFillColor(white)#phil membeship
            c.rect(6.3*inch,7.27*inch,0.09*inch,0.09*inch,fill=1)#Direct Contributor
        if phil_mem == 'INDIRECT CONTRIBUTOR':
            c.setFillColor(black)#phil membeship
            c.rect(6.3*inch,7.14*inch,0.09*inch,0.09*inch,fill=1)#InDirect Contributor
        else:
            c.setFillColor(white)#phil membeship
            c.rect(6.3*inch,7.14*inch,0.09*inch,0.09*inch,fill=1)#InDirect Contributor


        c.setFillColor("black")# naming con. hea
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(6.42*inch, 7.27*inch, "Direct Contributor")
        c.drawString(6.42*inch, 7.14*inch, "Indirect Contributor")       

        c.setFillColor(white)#16
        c.rect(0.25*inch,6.95*inch,7.75*inch,0.15*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(3.3*inch, 6.98*inch, "FAMILY COMPOSITIOM")

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(0.25*inch,6.75*inch,2.2*inch,0.2*inch,fill=1)
        c.rect(2.45*inch,6.75*inch,0.4*inch,0.2*inch,fill=1)
        c.rect(2.85*inch,6.75*inch,1*inch,0.2*inch,fill=1)
        c.rect(3.85*inch,6.75*inch,1*inch,0.2*inch,fill=1)
        c.rect(4.85*inch,6.75*inch,1*inch,0.2*inch,fill=1)
        c.rect(5.85*inch,6.75*inch,1*inch,0.2*inch,fill=1)
        c.rect(6.85*inch,6.75*inch,1.15*inch,0.2*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(1.21*inch, 6.77*inch, "NAME")
        c.drawString(2.5*inch, 6.77*inch, "AGE")
        c.drawString(2.95*inch, 6.77*inch, "CIVIL STATUS")
        c.drawString(6*inch, 6.77*inch, "OCCUPATION")
        c.drawString(6.9*inch, 6.77*inch, "MONTHLY INCOME")
        c.setFont("Times-Roman", 6.5, leading=None)
        c.drawString(3.86*inch, 6.77*inch, "RELATION TO PATIENT")
        c.drawString(5*inch, 6.86*inch, "EDUCATIONAL")
        c.drawString(5*inch, 6.78*inch, "ATTAINMENT")


        c.setLineWidth(1)
        c.setFillColor(white)

        a =0.15
        b = 6.6
        for i in range(10):
            c.rect(0.25*inch,b*inch,2.2*inch,0.15*inch,fill=1)
            c.rect(2.45*inch,b*inch,0.4*inch,0.15*inch,fill=1)
            c.rect(2.85*inch,b*inch,1*inch,0.15*inch,fill=1)
            c.rect(3.85*inch,b*inch,1*inch,0.15*inch,fill=1)
            c.rect(4.85*inch,b*inch,1*inch,0.15*inch,fill=1)
            c.rect(5.85*inch,b*inch,1*inch,0.15*inch,fill=1)
            c.rect(6.85*inch,b*inch,1.15*inch,0.15*inch,fill=1)
            b -= a

        famcom = FamilyComposition.objects.filter(uis = uis)
        pp =0.15
        tt = 6.62
        for cc in famcom:
            c.setFillColor("black")
            c.setFont("Times-Bold", 6.5, leading=None)
            c.drawString(0.27*inch, tt *inch, cc.fullname)
            c.drawString(2.47*inch, tt *inch, cc.age)
            c.drawString(2.87*inch, tt *inch, cc.cstat)
            c.drawString(3.87*inch, tt *inch, cc.relation_to_patient)
            c.drawString(4.87*inch, tt *inch, cc.hea)
            c.setFillColor("black")
            c.setFont("Times-Bold", 5, leading=None)
            c.drawString(5.87*inch, tt *inch, cc.occupation)
            c.setFillColor("black")
            c.setFont("Times-Bold", 6.5, leading=None)
            famcom_mi = '{:,.2f}'.format(float(cc.mi))
            c.drawString(6.87*inch, tt *inch, famcom_mi)
            tt -=pp
        
        c.setLineWidth(1)
        c.setFillColor(whitesmoke)
        c.rect(0.25*inch,5.1*inch,3.6*inch,0.15*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,4.65*inch,3.6*inch,0.45*inch,fill=1)


        xe = 0.15
        ye = 4.97
        famcom_osof = Fc_other_source.objects.filter(uis = uis)
        for fo in famcom_osof:
            c.setFillColor("black")
            c.setFont("Times-Bold", 6.5, leading=None)
            c.drawString(0.4*inch, ye*inch, fo.otherSources_of_fi_desc)
            tot_income_osof = '{:,.2f}'.format(float(fo.otherSources_of_fi))
            c.drawString(3*inch, ye*inch, tot_income_osof)
            ye -= xe

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.5*inch, 5.12*inch, "OTHER SOURCES OF INCOME")
        c.drawString(3*inch, 5.12*inch, "AMOUNT")
        

        c.setLineWidth(1)
        c.setFillColor(whitesmoke)
        c.rect(3.85*inch,4.65*inch,0.6*inch,0.6*inch,fill=1)
        c.setFillColor(white)
        c.rect(4.45*inch,4.65*inch,0.6*inch,0.6*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(4.67*inch, 4.95*inch, hsize)

        c.setFillColor(whitesmoke)
        c.rect(5.05*inch,4.65*inch,0.7375*inch,0.6*inch,fill=1)
        c.setFillColor(white)
        c.rect(5.7875*inch,4.65*inch,0.7375*inch,0.6*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 7, leading=None)
        total_incomes = '{:,.2f}'.format(float(tot_income))
        c.drawString(5.9*inch, 4.95*inch, total_incomes)

        c.setFillColor(whitesmoke)
        c.rect(6.525*inch,4.65*inch,0.7375*inch,0.6*inch,fill=1)
        c.setFillColor(white)
        c.rect(7.2625*inch,4.65*inch,0.7375*inch,0.6*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 7, leading=None)
        total_pci = '{:,.2f}'.format(float(per_capita_income ))
        c.drawString(7.4*inch, 4.95*inch, total_pci)

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(3.9*inch, 4.97*inch, "Household")
        c.drawString(3.9*inch, 4.85*inch, "Size:")
        c.drawString(5.1*inch, 4.97*inch, "Total Family")
        c.drawString(5.1*inch, 4.85*inch, "Income:")
        c.drawString(6.6*inch, 4.97*inch, "Per Capita")
        c.drawString(6.6*inch, 4.85*inch, "Income:")

        c.setFillColor(skyblue)#II.MSWD CLASSIFICATION
        c.rect(0.25*inch,4.5*inch,7.75*inch,0.15*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 4.52*inch, "II. MSWD CLASSIFICATION")

        c.setFillColor(white)#II.MSWD CLASSIFICATION
        c.rect(1.25*inch,4.2*inch,2.6*inch,0.3*inch,fill=1)
        c.rect(1.25*inch,3.6*inch,2.6*inch,0.6*inch,fill=1)
        c.rect(4.85*inch,3.6*inch,3.15*inch,0.9*inch,fill=1)

        c.setFillColor(whitesmoke)#MainCLASSIFICATION
        c.rect(0.25*inch,4.2*inch,1*inch,0.3*inch,fill=1)
        c.rect(0.25*inch,3.6*inch,1*inch,0.6*inch,fill=1)
        c.rect(3.85*inch,3.6*inch,1*inch,0.9*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 7.5, leading=None)
        c.drawString(0.3*inch, 4.32*inch, "Main Classification")
        c.drawString(0.3*inch, 4.05*inch, "Sub Classification for")
        c.drawString(0.3*inch, 3.95*inch, "Non Philhealth")
        c.drawString(0.3*inch, 3.85*inch, "Covered")
        c.drawString(0.3*inch, 3.75*inch, "Admission Procedure")

        c.drawString(4*inch, 4.2*inch, "Membership to")
        c.drawString(4*inch, 4.1*inch, "Marginalized")
        c.drawString(4*inch, 4*inch, "Sector")

        if mswd_cat == 'C1':
            c.setFillColor(black)
            c.rect(1.5*inch,4.41*inch,0.07*inch,0.07*inch,fill=1)#box financially Capable
        else:
            c.setFillColor(white)
            c.rect(1.5*inch,4.41*inch,0.07*inch,0.07*inch,fill=1)#box financially Capable
        if mswd_cat == 'C2':
            c.setFillColor(black)
            c.rect(1.5*inch,4.32*inch,0.07*inch,0.07*inch,fill=1)#box financially InCapable
        else:
            c.setFillColor(white)
            c.rect(1.5*inch,4.32*inch,0.07*inch,0.07*inch,fill=1)#box financially InCapable
        if mswd_cat == 'C3':
            c.setFillColor(black)
            c.rect(1.5*inch,4.22*inch,0.07*inch,0.07*inch,fill=1)#box idigent people
        else:
            c.setFillColor(white)
            c.rect(1.5*inch,4.22*inch,0.07*inch,0.07*inch,fill=1)#box idigent people

        c.setFillColor("black")
        c.setFont("Times-Roman", 6, leading=None)
        c.drawString(1.7*inch, 4.41*inch, "Financially Capable/Capacitated(4,544 & up)")
        c.drawString(1.7*inch, 4.32*inch, "Financially InCapable/InCapacitated(2,892 & 4,543)")
        c.drawString(1.7*inch, 4.22*inch, "Indigent(2,891 & below)")

        c.setFillColor("black")
        c.setFont("Times-Bold", 12, leading=None)
        c.drawString(1.5*inch, 3.98*inch, "C1")
        c.drawString(2.4*inch, 3.98*inch, "C2")
        c.drawString(3.3*inch, 3.98*inch, "C3")

        c.setFillColor("black")
        c.setFont("Times-Roman", 6, leading=None)
        c.drawString(1.35*inch, 3.87*inch, "(3,718-4,543)")
        c.drawString(2.25*inch, 3.87*inch, "(2,892-3,717)")
        c.drawString(3.17*inch, 3.87*inch, "(2,606-2,891)")

        if mswd_cat == 'C1':
            c.setFillColor(black)
            c.rect(1.52*inch,3.7*inch,0.1*inch,0.1*inch,fill=1)#box c1
        else:
            c.setFillColor(white)
            c.rect(1.52*inch,3.7*inch,0.1*inch,0.1*inch,fill=1)#box c1
        if mswd_cat == 'C2':
            c.setFillColor(black)
            c.rect(2.39*inch,3.7*inch,0.1*inch,0.1*inch,fill=1)#box c2
        else:
            c.setFillColor(white)
            c.rect(2.39*inch,3.7*inch,0.1*inch,0.1*inch,fill=1)#box c2
        if mswd_cat == 'C3':
            c.setFillColor(black)
            c.rect(3.34*inch,3.7*inch,0.1*inch,0.1*inch,fill=1)#box c3
        else:
            c.setFillColor(white)
            c.rect(3.34*inch,3.7*inch,0.1*inch,0.1*inch,fill=1)#box c3

        c.setFillColor("black")
        c.setFont("Times-Roman", 6, leading=None)
        c.drawString(5.1*inch, 4.3*inch, "Artisanal Fishfolk")
        c.drawString(5.1*inch, 4.2*inch, "Farmer and Landless Rural Worker")
        c.drawString(5.1*inch, 4.1*inch, "Urban Poor")
        c.drawString(5.1*inch, 4*inch, "Indegenous Peoples")
        c.drawString(5.1*inch, 3.9*inch, "Senior Citizen")
        c.drawString(5.1*inch, 3.8*inch, "Formal Labor and Migrant Workers")
        c.drawString(5.1*inch, 3.7*inch, "Workers in Informal Sector")
        c.drawString(6.7*inch, 4.3*inch, "PWD")
        c.drawString(6.7*inch, 4.2*inch, "Victims of Disaster and Calamity")
        c.drawString(6.7*inch, 4.1*inch, "Others:(Specify)")

        if marginalized_sec_mem == 'ARTISANAL FISHERFOLK':
            c.setFillColor(black)
            c.rect(4.9*inch,4.3*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        else:
            c.setFillColor(white)
            c.rect(4.9*inch,4.3*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        if marginalized_sec_mem == 'FARMERS AND LANDLESS RURAL WORKERS':
            c.setFillColor(black)
            c.rect(4.9*inch,4.2*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        else:
            c.setFillColor(white)
            c.rect(4.9*inch,4.2*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        if marginalized_sec_mem == 'URBAN POOR':
            c.setFillColor(black)
            c.rect(4.9*inch,4.1*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        else:
            c.setFillColor(white)
            c.rect(4.9*inch,4.1*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        if marginalized_sec_mem == 'INDIGENOUS PEOPLE':
            c.setFillColor(black)
            c.rect(4.9*inch,4*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        else:
            c.setFillColor(white)
            c.rect(4.9*inch,4*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        if marginalized_sec_mem == 'SENIOR CITIZEN':
            c.setFillColor(black)
            c.rect(4.9*inch,3.9*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        else:
            c.setFillColor(white)
            c.rect(4.9*inch,3.9*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        if marginalized_sec_mem == 'FORMAL AND LABOR MIGRANT WORKERS':
            c.setFillColor(black)
            c.rect(4.9*inch,3.8*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        else:
            c.setFillColor(white)
            c.rect(4.9*inch,3.8*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        if marginalized_sec_mem == 'WORKERS IN INFORMAL SECTORS':
            c.setFillColor(black)
            c.rect(4.9*inch,3.7*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        else:
            c.setFillColor(white)
            c.rect(4.9*inch,3.7*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        if marginalized_sec_mem == 'PWD':
            c.setFillColor(black)
            c.rect(6.5*inch,4.3*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        else:
            c.setFillColor(white)
            c.rect(6.5*inch,4.3*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        if marginalized_sec_mem == 'VICTIMS OF DISASTERS AND CALAMTIES':
            c.setFillColor(black)
            c.rect(6.5*inch,4.2*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        else:
            c.setFillColor(white)
            c.rect(6.5*inch,4.2*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        if marginalized_sec_mem == 'OTHERS':
            c.setFillColor(black)
            c.rect(6.5*inch,4.1*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        else:
            c.setFillColor(white)
            c.rect(6.5*inch,4.1*inch,0.08*inch,0.08*inch,fill=1)#box membership marginalized sector
        
        c.setFillColor(skyblue)#III.MONTHLY EXPENSE
        c.rect(0.25*inch,3.45*inch,7.75*inch,0.15*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 3.47*inch, "III. MONTHLY EXPENSES")

        c.setFillColor(white)#monthly expense
        c.rect(1.25*inch,2.45*inch,2.6*inch,1*inch,fill=1)
        c.rect(1.25*inch,2.45*inch,0.8*inch,1*inch,fill=1)
        c.rect(3.05*inch,2.45*inch,0.8*inch,1*inch,fill=1)
        
        c.setFillColor(whitesmoke)#monthly expense
        c.rect(0.25*inch,2.45*inch,1*inch,1*inch,fill=1)
        c.rect(2.05*inch,2.45*inch,1*inch,1*inch,fill=1)
        c.rect(0.25*inch,3.3*inch,1*inch,0.15*inch,fill=1)#particulars
        c.rect(1.25*inch,3.3*inch,0.8*inch,0.15*inch,fill=1)#estimated Momnthly cost (php)
        c.rect(2.05*inch,3.3*inch,1*inch,0.15*inch,fill=1)#particulars
        c.rect(3.05*inch,3.3*inch,0.8*inch,0.15*inch,fill=1)#estimated Momnthly cost
     
        c.setFillColor("black")
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(0.5*inch, 3.35*inch, "Particulars")
        c.drawString(2.35*inch, 3.35*inch, "Particulars")
        c.drawString(0.3*inch, 3.2*inch, "Food")
        c.drawString(0.3*inch, 3.05*inch, "Education")
        c.drawString(0.3*inch, 2.9*inch, "Clothing")
        c.drawString(0.3*inch, 2.77*inch, "Transportation")
        c.drawString(0.3*inch, 2.62*inch, "Househelp")
        c.drawString(0.3*inch, 2.47*inch, "TOTAL:")
        c.drawString(2.1*inch, 3.2*inch, "Medical Expenditure")
        c.drawString(2.1*inch, 3.05*inch, "Insurance Premium")
        c.drawString(2.1*inch, 2.9*inch, "Others")
        

        c.setFillColor("black")
        c.setFont("Times-Bold", 5, leading=None)
        c.drawString(1.27*inch, 3.35*inch, "Estimated Monthly Cost")
        c.drawString(3.07*inch, 3.35*inch, "Estimated Monthly Cost")

        c.setFillColor(white)#monthly expense
        c.rect(3.85*inch,2.45*inch,1.15*inch,1*inch,fill=1)
        c.rect(5*inch,2.45*inch,1.5*inch,1*inch,fill=1)
        c.rect(6.5*inch,2.45*inch,1.5*inch,1*inch,fill=1)

        c.setFillColor(whitesmoke)# water source
        c.rect(3.85*inch,2.45*inch,0.575*inch,1*inch,fill=1)#light source
        c.rect(5*inch,2.45*inch,0.75*inch,1*inch,fill=1)#fuel source
        c.rect(6.5*inch,2.45*inch,0.75*inch,1*inch,fill=1)#water source

        c.setFillColor(whitesmoke)
        c.rect(3.85*inch,3.3*inch,1.15*inch,0.15*inch,fill=1)#light source, fuel source, water source
        c.rect(5*inch,3.3*inch,1.5*inch,0.15*inch,fill=1)
        c.rect(6.5*inch,3.3*inch,1.5*inch,0.15*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(4.15*inch, 3.35*inch, "Light Source")
        c.drawString(5.5*inch, 3.35*inch, "Fuel Source")
        c.drawString(6.9*inch, 3.35*inch, "Water Source")

        c.setFillColor("black")
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(4*inch, 3.15*inch, "Electric")
        c.drawString(4*inch, 2.88*inch, "Kerosene")
        c.drawString(4*inch, 2.61*inch, "Candle")

        c.setFillColor("black")
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(5.14*inch, 3.15*inch, "Gas")
        c.drawString(5.14*inch, 2.88*inch, "FIREWOOD")
        c.drawString(5.14*inch, 2.61*inch, "CHARCOAL")

        c.setFillColor("black")
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.64*inch, 3.12*inch, "Artisan Well")
        c.drawString(6.64*inch, 2.9*inch, "Public")
        c.drawString(6.64*inch, 2.69*inch, "Private")
        c.drawString(6.64*inch, 2.51*inch, "Water District")

        c.setLineWidth(1)# horizontalline bottom monthly expense
        c.line(0.25*inch,3.16*inch,3.85*inch,3.16*inch)
        c.line(0.25*inch,3.02*inch,6.5*inch,3.02*inch)
        c.line(0.25*inch,2.88*inch,3.85*inch,2.88*inch)
        c.line(0.25*inch,2.74*inch,6.5*inch,2.74*inch)
        c.line(0.25*inch,2.6*inch,3.85*inch,2.6*inch)
        c.line(6.5*inch,3.07*inch,8*inch,3.07*inch)
        c.line(6.5*inch,2.85*inch,8*inch,2.85*inch)
        c.line(6.5*inch,2.65*inch,8*inch,2.65*inch)
       
        c.setLineWidth(1)
        c.setFillColor(white)
        list_of_expenses = ListofExpenses.objects.filter(uis = uis)
        for  oo in list_of_expenses:
            hauz = oo.house
            amt_hauz = oo.amt_house
            ls = oo.ligth_source
            amt_ls = oo.amt_ligth_source
            conv_ls = ls.replace("[","").replace("]","").replace("'","")
            conv_amt_ls = amt_ls.replace("[","").replace("]","").replace("'","")
            f_fls = conv_ls.replace(" ","")
            fls=f_fls.split(',')
            amt_fls = conv_amt_ls.split(',')
            ws = oo.water_source
            amt_ws = oo.amt_water_source
            conv_ws = ws.replace("[","").replace("]","").replace("'","")
            conv_amt_ws = amt_ws.replace("[","").replace("]","").replace("'","")
            f_fws = conv_ws.replace(" ","")
            fws=f_fws.split(',')
            amt_fws = conv_amt_ws.split(',')
            oth_expenses = oo.other_expenses
            amt_oth_expenses = oo.amt_other_expenses
            conv_amt_oth_expenses= amt_oth_expenses.replace("[","").replace("]","").replace("'","")
            conv_oth_expenses = oth_expenses.replace("[","").replace("]","").replace("'","")
            f_oe = conv_oth_expenses.replace(" ","")
            oe = f_oe.split(',')
            amt_oe = conv_amt_oth_expenses.split(',')

        c.setLineWidth(1)
        if fls[0] == 'ELECTRICITY':
            c.setFillColor(black)
            c.rect(3.88*inch,3.15*inch,0.08*inch,0.08*inch,fill=1)# electricty
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(4.5*inch, 3.15*inch, amt_fls[0])
        else:
            c.setFillColor(white)
            c.rect(3.88*inch,3.15*inch,0.08*inch,0.08*inch,fill=1)# electricty
        
        if fls[1] == 'KEROSENE':
            c.setFillColor(black)
            c.rect(3.88*inch,2.88*inch,0.08*inch,0.08*inch,fill=1)# kerosene
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(4.5*inch, 2.88*inch, amt_fls[1])
        else:
            c.setFillColor(white)
            c.rect(3.88*inch,2.88*inch,0.08*inch,0.08*inch,fill=1)# kerosene

        if fls[2] == 'CANDLE':
            c.setFillColor(black)
            c.rect(3.88*inch,2.61*inch,0.08*inch,0.08*inch,fill=1)# candle
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(4.5*inch, 2.61*inch, amt_fls[2])
        else:
            c.setFillColor(white)
            c.rect(3.88*inch,2.61*inch,0.08*inch,0.08*inch,fill=1)# candle


        c.setFillColor("black")
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.64*inch, 3.12*inch, "Artisan Well")
        c.drawString(6.64*inch, 2.9*inch, "Public")
        c.drawString(6.64*inch, 2.69*inch, "Private")
        c.drawString(6.64*inch, 2.51*inch, "Water District")
   
        c.setLineWidth(1)
        if fws[0] == 'PUBLIC':
            c.setFillColor(black)
            c.rect(6.53*inch,2.9*inch,0.08*inch,0.08*inch,fill=1)# public
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(7.3*inch, 2.9*inch, amt_fws[0])
        else:
            c.setFillColor(white)
            c.rect(6.53*inch,2.9*inch,0.08*inch,0.08*inch,fill=1)# public

        if fws[1] == 'NATURAL':
            c.setFillColor(black)
            c.rect(6.53*inch,3.12*inch,0.08*inch,0.08*inch,fill=1)# artisan well
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(7.3*inch, 3.12*inch, amt_fws[1])
        else:
            c.setFillColor(white)
            c.rect(6.53*inch,3.12*inch,0.08*inch,0.08*inch,fill=1)# artisan well

        if fws[2] == 'WATERDISTRICT':
            c.setFillColor(black)
            c.rect(6.53*inch,2.51*inch,0.08*inch,0.08*inch,fill=1)# water district
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(7.3*inch, 2.51*inch, amt_fws[2])
        else:
            c.setFillColor(white)
            c.rect(6.53*inch,2.51*inch,0.08*inch,0.08*inch,fill=1)# water district
        if fws[3] == 'MINERAL':
            c.setFillColor(black)
            c.rect(6.53*inch,2.69*inch,0.08*inch,0.08*inch,fill=1)# private
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(7.3*inch, 2.69*inch, amt_fws[3])
        else:
            c.setFillColor(white)
            c.rect(6.53*inch,2.69*inch,0.08*inch,0.08*inch,fill=1)# private

      
        if fuel_src[0]=='LPG':
            c.setFillColor(black)
            c.rect(5.03*inch,3.15*inch,0.08*inch,0.08*inch,fill=1)# Gas
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(5.8*inch, 3.15*inch, amt_fuel_src[0])
        else:
            c.setFillColor(white)
            c.rect(5.03*inch,3.15*inch,0.08*inch,0.08*inch,fill=1)# Gas
        # if fuel_src[1]=='ELECTRIC':
        #     c.setFillColor(black)
        #     c.rect(6.12*inch,2.4*inch,0.12*inch,0.12*inch,fill=1)
        #     c.setFont("Times-Bold", 7, leading=None)
        #     c.drawString(7.12*inch, 2.43*inch, amt_fuel_src[1])
        # else:
        #     c.setFillColor(white)
        #     c.rect(6.12*inch,2.4*inch,0.12*inch,0.12*inch,fill=1)
        if fuel_src[1]=='CHARCOAL':
            c.setFillColor(black)
            c.rect(5.03*inch,2.88*inch,0.08*inch,0.08*inch,fill=1)# Firewood
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(5.8*inch, 2.88*inch, amt_fuel_src[1])
        else:
            c.setFillColor(white)
            c.rect(5.03*inch,2.88*inch,0.08*inch,0.08*inch,fill=1)# Firewood
        if fuel_src[2]=='FIREWOOD':
            c.setFillColor(black)
            c.rect(5.03*inch,2.61*inch,0.08*inch,0.08*inch,fill=1)# CHarcoal
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(5.8*inch, 2.61*inch, amt_fuel_src[2])
        else:
            c.setFillColor(white)
            c.rect(5.03*inch,2.61*inch,0.08*inch,0.08*inch,fill=1)# CHarcoal


        c.setFillColor(black)
        c.setFont("Times-Bold", 8, leading=None)
        tot_expense_cloth = float(tot_expense) + float(clothing_amt)
        total_exp = '{:,.2f}'.format(float(tot_expense_cloth))
        c.drawString(1.3*inch, 2.47*inch, total_exp)
        # c.setLineWidth(1)
        # c.drawString(0.5*inch, 3.35*inch, "Particulars")
        # c.drawString(2.35*inch, 3.35*inch, "Particulars")
        # c.drawString(0.3*inch, 3.2*inch, "Food")
        # c.drawString(0.3*inch, 3.05*inch, "Education")
        # c.drawString(0.3*inch, 2.9*inch, "Clothing")
        # c.drawString(0.3*inch, 2.77*inch, "Transportation")
        # c.drawString(0.3*inch, 2.62*inch, "Househelp")
        # c.drawString(0.3*inch, 2.47*inch, "TOTAL:")
        # c.drawString(2.1*inch, 3.2*inch, "Medical Expenditure")
        # c.drawString(2.1*inch, 3.05*inch, "Insurance Premium")
        # c.drawString(2.1*inch, 2.9*inch, "Others")
        if oe[0] == 'HOUSE':
            c.setFillColor("black")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.3*inch, 2.62*inch, amt_oe[0])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.3*inch, 2.62*inch,"0.00")
        
        if oe[3] == 'EDU':
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.3*inch, 3.05*inch, amt_oe[3])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.3*inch, 3.05*inch, "0.00")
        if oe[6] == 'FOOD':
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.3*inch, 3.2*inch, amt_oe[6])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.3*inch, 3.2*inch, "0.00")

        if clothing_amt is not None:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.3*inch, 2.9*inch, clothing_amt)
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.3*inch, 2.9*inch, "0.00")

        if oe[1] == 'ME':
            c.setFillColor("black")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(3.26*inch, 3.2*inch, amt_oe[1])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(3.26*inch, 3.2*inch, "0.00")

        if oe[2] == 'IP':
            c.setFillColor("black")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(3.26*inch, 3.05*inch, amt_oe[2])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(3.26*inch, 3.05*inch, "0.00")
        if oe[5] == 'TRANSPO':
            c.setFillColor(black)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(1.3*inch, 2.77*inch, amt_oe[5])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(1.3*inch, 2.77*inch, "0.00")

        if oe[8] == 'OTHER':
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(3.26*inch, 2.9*inch, amt_oe[8])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(3.26*inch, 2.9*inch, "0.00")

        c.setFillColor(skyblue)
        c.rect(0.25*inch,2.3*inch,7.75*inch,0.15*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.28*inch, 2.32*inch, "IV. MEDICAL HISTORY")
       
        c.setFillColor(white)
        c.rect(0.25*inch,2.05*inch,3.875*inch,0.25*inch,fill=1)
        c.rect(4.125*inch,2.05*inch,3.875*inch,0.25*inch,fill=1)
        c.setFillColor(whitesmoke)
        c.rect(0.25*inch,2.2*inch,3.875*inch,0.1*inch,fill=1)
        c.rect(4.125*inch,2.2*inch,3.875*inch,0.1*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 6, leading=None)
        c.drawString(0.28*inch, 2.22*inch, "ADMITTING DIAGNOSIS")
        c.drawString(4.15*inch, 2.22*inch, "FINAL DIAGNOSIS")

        c.setFillColor(white)
        c.rect(0.25*inch,1.8*inch,3.875*inch,0.25*inch,fill=1)
        c.rect(4.125*inch,1.8*inch,3.875*inch,0.25*inch,fill=1)
        c.setFillColor(whitesmoke)
        c.rect(0.25*inch,1.95*inch,3.875*inch,0.1*inch,fill=1)
        c.rect(4.125*inch,1.95*inch,3.875*inch,0.1*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 6, leading=None)
        c.drawString(0.28*inch, 1.97*inch, "DURATION OF PROBLEM/SYMPTOMS")
        c.drawString(4.15*inch, 1.97*inch, "PREVIOUS TREATMENT/DURATION")

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        p = Paragraph(duration_of_prob, style=custom_font_size)
        p.wrapOn(c, 270,20)  
        p.drawOn(c,0.3*inch,1.82*inch) 
        p = Paragraph(prev_treatment, style=custom_font_size)
        p.wrapOn(c, 270,20)  
        p.drawOn(c,4.2*inch,1.82*inch) 

        c.setFillColor(white)
        c.rect(0.25*inch,1.55*inch,3.875*inch,0.25*inch,fill=1)
        c.rect(4.125*inch,1.55*inch,3.875*inch,0.25*inch,fill=1)
        c.setFillColor(whitesmoke)
        c.rect(0.25*inch,1.7*inch,3.875*inch,0.1*inch,fill=1)
        c.rect(4.125*inch,1.7*inch,3.875*inch,0.1*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 6, leading=None)
        c.drawString(0.28*inch, 1.72*inch, "PRESENT TREATMENT PLAN:")
        c.drawString(4.15*inch, 1.72*inch, "HEALTH ACCESSIBILITY PROBLEM")

        c.setFillColor(black)
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 1.57*inch,"CONFINEMENT")

        p = Paragraph(health_accessibility_prob, style=custom_font_size)
        p.wrapOn(c, 270,20)  
        p.drawOn(c,4.2*inch,1.57*inch) 

        problem_presented = ProblemPresented.objects.filter(uis = uis)
        for mm in problem_presented:
            problem = mm.problem
            conv_problem = problem.replace("[","").replace("]","").replace("'","")
            f_problem = conv_problem.replace(" ","")
            fproblem = f_problem.split(',')
            prob_desc = mm.prob_desc
            conv_prob_desc = prob_desc.replace("[","").replace("]","").replace("'","")
            f_prob_desc = conv_prob_desc.split(',') 

            p = Paragraph(f_prob_desc[0], style=custom_font_size)
            p.wrapOn(c, 270,20)  
            p.drawOn(c,0.3*inch,2.07*inch) 

            p = Paragraph(f_prob_desc[0], style=custom_font_size)
            p.wrapOn(c, 270,20)  
            p.drawOn(c,4.2*inch,2.07*inch) 

        c.setFillColor(white)
        c.rect(0.25*inch,1.15*inch,3.875*inch,0.4*inch,fill=1)
        c.rect(4.125*inch,1.15*inch,3.875*inch,0.4*inch,fill=1)
        c.setFillColor(whitesmoke)
        c.rect(0.25*inch,1.45*inch,3.875*inch,0.1*inch,fill=1)
        c.rect(4.125*inch,1.45*inch,3.875*inch,0.1*inch,fill=1)
        swa_desc = SWA.objects.filter(uis = uis)
        for sw in swa_desc:
            desc_swa = sw.swa_desc
            p = Paragraph(desc_swa, style=custom_font_size_swa_first )
            p.wrapOn(c, 280,20)  
            p.drawOn(c,0.27*inch,1.19*inch) 
            p.wrapOn(c, 275,20) 
            p.drawOn(c,4.15*inch,1.19*inch) 


        c.setFillColor("black")
        c.setFont("Times-Roman", 6, leading=None)
        c.drawString(1.5*inch, 1.47*inch, "ASSESSMENT/FINDINGS")
        c.drawString(5.2*inch, 1.47*inch, "RECOMMENDED INTERVENTIONS")

        c.setFillColor(black)
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.3*inch, 1.05*inch,"Ako si                                                                             , nagsasabing naiintindihan ko na nag pag hingi namin ng tulong sa Medical Social Service ay naayon sa kinalabasan ng Interview ng Social")
        c.drawString(0.3*inch, 0.95*inch,"Worker sa amin. Anumang maling impormasyon na ibinigay namin ay pwedeng dahilan para mapawalang bisa ang aming hinihinging tulong. Nang dahil dito, babayaran namin lahat ng bill ng")
        c.drawString(0.3*inch, 0.85*inch,"aming pasyente dito sa hospital.")
        c.drawString(0.6*inch, 1.05*inch, informant_fullname)
        c.setFillColor(black)
        c.setFont("Times-Bold", 5.5, leading=None)
        c.drawString(1*inch, 0.75*inch,"Conforme:")
        c.drawString(1.4*inch, 0.66*inch,"_________________________________________________________")
        c.drawString(1.4*inch, 0.56*inch,"SIGNATURE OF PATIENT/REPRESENTATIVE/COMPANION")
        c.drawString(5.2*inch, 0.66*inch,"___________________________________________________________")
        c.drawString(5.5*inch, 0.56*inch,"LICENSE NUMBER:")
   
     

        uwn = c.stringWidth(request.session['name'])/100
        uiwn = 210/100
        cun = (uiwn - uwn) / 2
        fxin = cun + 4.95
        c.drawString(fxin*inch, 0.65*inch, request.session['name'] )

        c.setFillColor(black)
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(4.1*inch, 0.45*inch,"Page 1")
        c.saveState()
        create_header(c, None)
        create_footer(c,None)
        c.restoreState()
        c.showPage()

    if page2 == 2:
        
        c.setStrokeColor(black)
        c.setLineWidth(1)# horizontalline top
        c.line(0.25*inch,10.45*inch,8*inch,10.45*inch)

        # c.setLineWidth(1)# horizontalline bottom
        # c.line(0.25*inch,0.55*inch,8*inch,0.55*inch)

        c.setLineWidth(1)# verticalline left
        c.line(0.25*inch,1.3*inch,0.25*inch,10.45*inch)

        c.setLineWidth(1)# verticalline right
        c.line(8*inch,1.3*inch,8*inch,10.45*inch)

        # c.setFillColor(skyblue)
        # c.rect(0.25*inch,10.3*inch,7.75*inch,0.15*inch,fill=1)
        # c.setFillColor("black")
        # c.setFont("Times-Bold", 8, leading=None)
        # c.drawString(0.28*inch, 10.32*inch, "II. ASSESSMENT OF SOCIAL FUNCTIONING")

        # c.setFillColor(white)
        # c.rect(0.25*inch,7.3*inch,7.75*inch,2*inch,fill=1)


        c.setFillColor("black")
        c.setFont("Times-Roman", 7.7, leading=None)
        c.drawString(0.4*inch, 10.3*inch, "1.   FAMILIAL ROLES")
        c.drawString(1.82*inch, 10.3*inch, "TYPE OF SOCIAL INTERACTION")
        c.drawString(1.82*inch, 10.15*inch, "PROBLEM")
        c.drawString(1.82*inch, 10*inch, "1. POWER")
        c.drawString(1.82*inch, 9.85*inch, "2. AMBIVALENCE")
        c.drawString(1.82*inch, 9.65*inch, "3. RESPONSIBILITY")
        c.drawString(1.82*inch, 9.45*inch, "4. DEPENDENCY")
        c.drawString(1.82*inch, 9.25*inch, "5. LOSS")
        c.drawString(1.82*inch, 9.1*inch, "6. ISOLATION")
        c.drawString(1.82*inch, 8.9*inch, "7. VICTIMIZATION")
        c.drawString(1.82*inch, 8.75*inch, "8. MIXED")
        # c.drawString(1.82*inch, 8.5*inch, "9. OTHERS")

        c.drawString(3.62*inch, 10.3*inch, "SECERITY INDEX")
        c.drawString(3.64*inch, 10.15*inch, "1. NO PROBLEM")
        c.drawString(3.64*inch, 10*inch, "2. LOW")
        c.drawString(3.64*inch, 9.85*inch, "3. MODERATE")
        c.drawString(3.64*inch, 9.65*inch, "4. HIGH")
        c.drawString(3.64*inch, 9.45*inch, "5. VERY HIGH")
        c.drawString(3.64*inch, 9.25*inch, "6. CATASTROPHIC")
        
        c.drawString(5.22*inch, 10.3*inch, "DURATION INDEX")
        c.drawString(5.24*inch, 10.15*inch, "1. More than five years")
        c.drawString(5.24*inch, 10*inch, "2. One to five years")
        c.drawString(5.24*inch, 9.85*inch, "3. Six mos to one Year")
        c.drawString(5.24*inch, 9.65*inch, "4. One to six mos")
        c.drawString(5.24*inch, 9.45*inch, "5. Two weeks to one month")
        c.drawString(5.24*inch, 9.25*inch, "6. Less than two weeks")

        c.drawString(6.62*inch, 10.3*inch, "COPING INDEX")
        c.drawString(6.64*inch, 10.15*inch, "1. Outstanding")
        c.drawString(6.64*inch, 10*inch, "2. Above average")
        c.drawString(6.64*inch, 9.85*inch, "3. Adequate")
        c.drawString(6.64*inch, 9.65*inch, "4. Somewhat Inadequate")
        c.drawString(6.64*inch, 9.45*inch, "5. Inadequate")
        c.drawString(6.64*inch, 9.25*inch, "6. No coping skills")

        c.setLineWidth(1)# verticalline left 1st
        c.line(1.8*inch,8.66*inch,1.8*inch,10.45*inch)
        c.line(3.6*inch,8.66*inch,3.6*inch,10.45*inch)
        c.line(5.2*inch,8.66*inch,5.2*inch,10.45*inch)
        c.line(6.6*inch,8.66*inch,6.6*inch,10.45*inch)
        
        bb = 0.15
        cc = 6.95
        for gg in range(7):
            c.setFillColor(white)#1 family roles
            c.rect(0.25*inch,cc*inch,7.75*inch,0.2*inch,fill=1)
            cc -= bb
        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.3*inch, 7.03*inch, "PARENT")
        c.drawString(0.3*inch, 6.88*inch, "SPOUSE")
        c.drawString(0.3*inch, 6.73*inch, "CHILD")
        c.drawString(0.3*inch, 6.58*inch, "SIBLING")
        c.drawString(0.3*inch, 6.43*inch, "OTHER FAMILY MEMBER")
        c.drawString(0.3*inch, 6.28*inch, "SIGNIFICANT OTHERS")

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 7.34*inch, "VI. ASSESSMENT OF SOCIAL FUNCTIONING")
        c.drawString(0.3*inch, 7.19*inch, "1.Family Roles")

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 6.12*inch, "2. Other Personal Roles")

        pi = 0.15
        li = 5.9
        for gg in range(5):
            c.setFillColor(white)#2. Other Personal Roles
            c.rect(0.25*inch,li*inch,7.75*inch,0.15*inch,fill=1)
            li-= pi

        c.setLineWidth(1)
        ll = 0.15    
        zz= 7.02
        for rr in range(6):
            c.setFillColor("black")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.88*inch, zz*inch, "1")
            c.drawString(3.7*inch, zz*inch, "1")
            c.drawString(5.29*inch, zz*inch, "1")
            c.drawString(6.7*inch, zz*inch, "1")
            c.drawString(2.105*inch, zz*inch, "2")
            c.drawString(2.31*inch, zz*inch, "3")
            c.drawString(2.535*inch, zz*inch, "4")
            c.drawString(2.76*inch, zz*inch, "5")
            c.drawString(2.985*inch, zz*inch, "6")
            c.drawString(3.21*inch, zz*inch, "7")
            c.drawString(3.435*inch, zz*inch, "8")
            c.drawString(3.95*inch, zz*inch, "2")
            c.drawString(5.52*inch, zz*inch, "2")
            c.drawString(6.9*inch, zz*inch, "2")
            c.drawString(4.2*inch, zz*inch, "3")
            c.drawString(5.75*inch, zz*inch, "3")
            c.drawString(7.15*inch, zz*inch, "3")
            c.drawString(4.45*inch, zz*inch, "4")
            c.drawString(5.99*inch, zz*inch, "4")
            c.drawString(7.4*inch, zz*inch, "4")
            c.drawString(4.75*inch, zz*inch, "5")
            c.drawString(6.25*inch, zz*inch, "5")
            c.drawString(7.64*inch, zz*inch, "5")
            c.drawString(5*inch, zz*inch, "6")
            c.drawString(6.48*inch, zz*inch, "6")
            c.drawString(7.88*inch, zz*inch, "6")
            zz-=ll

        xx = 0.15    
        cv= 5.94
        for rr in range(5):
            c.setFillColor("black")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.88*inch, cv*inch, "1")
            c.drawString(3.7*inch, cv*inch, "1")
            c.drawString(5.29*inch, cv*inch, "1")
            c.drawString(6.7*inch, cv*inch, "1")
            c.drawString(2.105*inch, cv*inch, "2")
            c.drawString(2.31*inch, cv*inch, "3")
            c.drawString(2.535*inch, cv*inch, "4")
            c.drawString(2.76*inch, cv*inch, "5")
            c.drawString(2.985*inch, cv*inch, "6")
            c.drawString(3.21*inch, cv*inch, "7")
            c.drawString(3.435*inch, cv*inch, "8")
            c.drawString(3.95*inch, cv*inch, "2")
            c.drawString(5.52*inch, cv*inch, "2")
            c.drawString(6.9*inch, cv*inch, "2")
            c.drawString(4.2*inch, cv*inch, "3")
            c.drawString(5.75*inch, cv*inch, "3")
            c.drawString(7.15*inch, cv*inch, "3")
            c.drawString(4.45*inch, cv*inch, "4")
            c.drawString(5.99*inch, cv*inch, "4")
            c.drawString(7.4*inch, cv*inch, "4")
            c.drawString(4.75*inch, cv*inch, "5")
            c.drawString(6.25*inch, cv*inch, "5")
            c.drawString(7.64*inch, cv*inch, "5")
            c.drawString(5*inch, cv*inch, "6")
            c.drawString(6.48*inch, cv*inch, "6")
            c.drawString(7.88*inch, cv*inch, "6")
            cv-=xx
       
        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.3*inch, 5.94*inch, "Lover")
        c.drawString(0.3*inch, 5.79*inch, "Friend")
        c.drawString(0.3*inch, 5.64*inch, "Neighbor")
        c.drawString(0.3*inch, 5.49*inch, "Member")
        c.drawString(0.3*inch, 5.34*inch, "Others (Specify)")

        
        
        wi = 0.15
        qi = 4.95
        for gg in range(5):
            c.setFillColor(white)#2. Other Personal Roles
            c.rect(0.25*inch,qi*inch,7.75*inch,0.15*inch,fill=1)
            qi-= wi
        

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 4.97*inch, "Woker-Paid Economy")
        c.drawString(0.3*inch, 4.82*inch, "Worker-Home")
        c.drawString(0.3*inch, 4.67*inch, "Worker-Volunteer")
        c.drawString(0.3*inch, 4.52*inch, "Student")
        c.drawString(0.3*inch, 4.37*inch, "Others(Specify)")

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 5.17*inch, "3.Occupational Roles")
        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 4.22*inch, "4. Special Life Situation Roles")

        rt=0.15
        qt=4.05
        for j in range(9):
            c.setFillColor(white)
            c.rect(0.25*inch,qt*inch,7.75*inch,0.15*inch,fill=1)
            qt -= rt

        my = 0.15    
        ny= 4.07
        for oq in range(9):
            c.setFillColor("black")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.88*inch, ny*inch, "1")
            c.drawString(3.7*inch, ny*inch, "1")
            c.drawString(5.29*inch, ny*inch, "1")
            c.drawString(6.7*inch, ny*inch, "1")
            c.drawString(2.105*inch, ny*inch, "2")
            c.drawString(2.31*inch, ny*inch, "3")
            c.drawString(2.535*inch, ny*inch, "4")
            c.drawString(2.76*inch, ny*inch, "5")
            c.drawString(2.985*inch, ny*inch, "6")
            c.drawString(3.21*inch, ny*inch, "7")
            c.drawString(3.435*inch, ny*inch, "8")
            c.drawString(3.95*inch, ny*inch, "2")
            c.drawString(5.52*inch, ny*inch, "2")
            c.drawString(6.9*inch, ny*inch, "2")
            c.drawString(4.2*inch, ny*inch, "3")
            c.drawString(5.75*inch, ny*inch, "3")
            c.drawString(7.15*inch, ny*inch, "3")
            c.drawString(4.45*inch, ny*inch, "4")
            c.drawString(5.99*inch, ny*inch, "4")
            c.drawString(7.4*inch, ny*inch, "4")
            c.drawString(4.75*inch, ny*inch, "5")
            c.drawString(6.25*inch, ny*inch, "5")
            c.drawString(7.64*inch, ny*inch, "5")
            c.drawString(5*inch, ny*inch, "6")
            c.drawString(6.48*inch, ny*inch, "6")
            c.drawString(7.88*inch, ny*inch, "6")
            ny-=my

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 4.07*inch, "Consumner")
        c.drawString(0.4*inch, 3.92*inch, "Inpatient/Client")
        c.drawString(0.4*inch, 3.77*inch, "Outpatient/Client")
        c.drawString(0.4*inch, 3.62*inch, "ER patient/Client")
        c.drawString(0.4*inch, 3.47*inch, "Prisoner")
        c.drawString(0.4*inch, 3.32*inch, "Immigrant-legal")
        c.drawString(0.4*inch, 3.17*inch, "Immigrant-undocumented")
        c.drawString(0.4*inch, 3.02*inch, "Immigrant-refuge")
        c.drawString(0.4*inch, 2.87*inch, "Others(Specify)")

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 2.72*inch, "5. Discrimination (CHECK ITEMS)")

        c.setFillColor(white)
        c.rect(0.25*inch,1.9*inch,7.75*inch,0.75*inch,fill=1)

        c.rect(0.4*inch,2.52*inch,0.09*inch,0.09*inch,fill=1)#box
        c.rect(1*inch,2.52*inch,0.09*inch,0.09*inch,fill=1)#box
        c.rect(2*inch,2.52*inch,0.09*inch,0.09*inch,fill=1)#box
        c.rect(3*inch,2.52*inch,0.09*inch,0.09*inch,fill=1)#box
        c.rect(0.4*inch,2.37*inch,0.09*inch,0.09*inch,fill=1)#box
        c.rect(1.7*inch,2.37*inch,0.09*inch,0.09*inch,fill=1)#box
        c.rect(2.7*inch,2.37*inch,0.09*inch,0.09*inch,fill=1)#box
        c.rect(0.4*inch,2.22*inch,0.09*inch,0.09*inch,fill=1)#box
        c.rect(1.7*inch,2.22*inch,0.09*inch,0.09*inch,fill=1)#box
        c.rect(0.4*inch,2.07*inch,0.09*inch,0.09*inch,fill=1)#box
        c.rect(1.7*inch,2.07*inch,0.09*inch,0.09*inch,fill=1)#box
        c.rect(0.4*inch,1.93*inch,0.09*inch,0.09*inch,fill=1)#box

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.5*inch, 2.52*inch, " Age               Ethnicity                     Religion                      Sex")
        c.drawString(0.5*inch, 2.37*inch, " Sexual Orientation               Lifestyle                     Non-Citizen")
        c.drawString(0.5*inch, 2.22*inch, " Veteran Status                      Dependency Status")
        c.drawString(0.5*inch, 2.07*inch, " Disability Status                   Marital Status")
        c.drawString(0.5*inch, 1.93*inch, " Others(specify)")

        aq=0.15
        zq=1.5
        for j in range(7):
            c.setFillColor(white)
            c.rect(0.25*inch,zq*inch,7.75*inch,0.15*inch,fill=1)
            zq -= aq
        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 1.7*inch, "VII. SAFETY")

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 1.52*inch, "Violence or Crime in Community")
        c.drawString(0.3*inch, 1.37*inch, "Unsafe Working Condition")
        c.drawString(0.3*inch, 1.22*inch, "Unsafe Conditions in Home")
        c.drawString(0.3*inch, 1.07*inch, "Absence of Adequate Safety Services")
        c.drawString(0.3*inch, 0.92*inch, "Natural Disaster")
        c.drawString(0.3*inch, 0.77*inch, "Human Created Disaster")
        c.drawString(0.3*inch, 0.62*inch, "Others (specify)")

        xy = 0.15    
        cy= 4.97
        for oo in range(5):
            c.setFillColor("black")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.88*inch, cy*inch, "1")
            c.drawString(3.7*inch, cy*inch, "1")
            c.drawString(5.29*inch, cy*inch, "1")
            c.drawString(6.7*inch, cy*inch, "1")
            c.drawString(2.105*inch, cy*inch, "2")
            c.drawString(2.31*inch, cy*inch, "3")
            c.drawString(2.535*inch, cy*inch, "4")
            c.drawString(2.76*inch, cy*inch, "5")
            c.drawString(2.985*inch, cy*inch, "6")
            c.drawString(3.21*inch, cy*inch, "7")
            c.drawString(3.435*inch, cy*inch, "8")
            c.drawString(3.95*inch, cy*inch, "2")
            c.drawString(5.52*inch, cy*inch, "2")
            c.drawString(6.9*inch, cy*inch, "2")
            c.drawString(4.2*inch, cy*inch, "3")
            c.drawString(5.75*inch, cy*inch, "3")
            c.drawString(7.15*inch, cy*inch, "3")
            c.drawString(4.45*inch, cy*inch, "4")
            c.drawString(5.99*inch, cy*inch, "4")
            c.drawString(7.4*inch, cy*inch, "4")
            c.drawString(4.75*inch, cy*inch, "5")
            c.drawString(6.25*inch, cy*inch, "5")
            c.drawString(7.64*inch, cy*inch, "5")
            c.drawString(5*inch, cy*inch, "6")
            c.drawString(6.48*inch, cy*inch, "6")
            c.drawString(7.88*inch, cy*inch, "6")
            cy-=xy

        ff=0.225
        ss=1.8
        for uu in range(8):
            c.line(ss*inch,7.15*inch,ss*inch,6.25*inch)
            c.line(ss*inch,6.05*inch,ss*inch,5.3*inch)
            c.line(ss*inch,5.09*inch,ss*inch,4.35*inch)
            c.line(ss*inch,4.2*inch,ss*inch,2.85*inch)
            ss+=ff
        v=0.15
        z=8.51
        for j in range(9):
            c.setFillColor(white)# health and mental health
            c.rect(0.25*inch,z*inch,7.75*inch,0.15*inch,fill=1)
            z -= v
        
        g=0.259
        d=3.6

        for k in range(6):
            c.setLineWidth(1)
            c.line(d*inch,7.45*inch,d*inch,8.51*inch)
            c.line(d*inch,6.25*inch,d*inch,7.15*inch)
            c.line(d*inch,6.05*inch,d*inch,5.3*inch)
            c.line(d*inch,5.09*inch,d*inch,4.35*inch)
            c.line(d*inch,4.2*inch,d*inch,2.85*inch)
            c.line(d*inch,1.65*inch,d*inch,0.6*inch)
            c.line(d*inch,2.65*inch,d*inch,1.9*inch)
            d +=g

        o=0.24
        p=5.2
      
        for l in range(6):
            c.setLineWidth(1)
            c.line(p*inch,7.45*inch,p*inch,8.51*inch)
            c.line(p*inch,6.25*inch,p*inch,7.15*inch)
            c.line(p*inch,6.05*inch,p*inch,5.3*inch)
            c.line(p*inch,5.09*inch,p*inch,4.35*inch)
            c.line(p*inch,4.2*inch,p*inch,2.85*inch)
            c.line(p*inch,1.65*inch,p*inch,0.6*inch)
            c.line(p*inch,2.65*inch,p*inch,1.9*inch)
            p +=o
        
        w=0.24
        q=6.6
        for l in range(6):
            c.setLineWidth(1)
            c.line(q*inch,7.45*inch,q*inch,8.51*inch)
            c.line(q*inch,6.25*inch,q*inch,7.15*inch)
            c.line(q*inch,6.05*inch,q*inch,5.3*inch)
            c.line(q*inch,5.09*inch,q*inch,4.35*inch)
            c.line(q*inch,4.2*inch,q*inch,2.85*inch)
            c.line(q*inch,1.65*inch,q*inch,0.6*inch)
            c.line(q*inch,2.65*inch,q*inch,1.9*inch)
            q +=w
        
        mq= 0.15
        nq= 2.3
        for gf in range(1):
            c.setFillColor("black")
            c.setFont("Times-Bold", 10, leading=None)
            c.drawString(3.7*inch, nq*inch, "1")
            c.drawString(5.29*inch, nq*inch, "1")
            c.drawString(6.7*inch, nq*inch, "1")
            c.drawString(3.95*inch, nq*inch, "2")
            c.drawString(5.52*inch, nq*inch, "2")
            c.drawString(6.9*inch, nq*inch, "2")
            c.drawString(4.2*inch, nq*inch, "3")
            c.drawString(5.75*inch, nq*inch, "3")
            c.drawString(7.15*inch, nq*inch, "3")
            c.drawString(4.45*inch, nq*inch, "4")
            c.drawString(5.99*inch, nq*inch, "4")
            c.drawString(7.4*inch, nq*inch, "4")
            c.drawString(4.75*inch, nq*inch, "5")
            c.drawString(6.25*inch, nq*inch, "5")
            c.drawString(7.64*inch, nq*inch, "5")
            c.drawString(5*inch, nq*inch, "6")
            c.drawString(6.48*inch, nq*inch, "6")
            c.drawString(7.88*inch, nq*inch, "6")
            nq-= mq
        m= 0.15
        n= 8.39
        for b in range(7):
            c.setFillColor("black")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(3.7*inch, n*inch, "1")
            c.drawString(5.29*inch, n*inch, "1")
            c.drawString(6.7*inch, n*inch, "1")
            c.drawString(3.95*inch, n*inch, "2")
            c.drawString(5.52*inch, n*inch, "2")
            c.drawString(6.9*inch, n*inch, "2")
            c.drawString(4.2*inch, n*inch, "3")
            c.drawString(5.75*inch, n*inch, "3")
            c.drawString(7.15*inch, n*inch, "3")
            c.drawString(4.45*inch, n*inch, "4")
            c.drawString(5.99*inch, n*inch, "4")
            c.drawString(7.4*inch, n*inch, "4")
            c.drawString(4.75*inch, n*inch, "5")
            c.drawString(6.25*inch, n*inch, "5")
            c.drawString(7.64*inch, n*inch, "5")
            c.drawString(5*inch, n*inch, "6")
            c.drawString(6.48*inch, n*inch, "6")
            c.drawString(7.88*inch, n*inch, "6")
            n -= m

        oy= 0.15
        oi= 1.52
        for b in range(7):
            c.setFillColor("black")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(3.7*inch, oi*inch, "1")
            c.drawString(5.29*inch, oi*inch, "1")
            c.drawString(6.7*inch, oi*inch, "1")
            c.drawString(3.95*inch, oi*inch, "2")
            c.drawString(5.52*inch, oi*inch, "2")
            c.drawString(6.9*inch, oi*inch, "2")
            c.drawString(4.2*inch, oi*inch, "3")
            c.drawString(5.75*inch, oi*inch, "3")
            c.drawString(7.15*inch, oi*inch, "3")
            c.drawString(4.45*inch, oi*inch, "4")
            c.drawString(5.99*inch, oi*inch, "4")
            c.drawString(7.4*inch, oi*inch, "4")
            c.drawString(4.75*inch, oi*inch, "5")
            c.drawString(6.25*inch, oi*inch, "5")
            c.drawString(7.64*inch, oi*inch, "5")
            c.drawString(5*inch, oi*inch, "6")
            c.drawString(6.48*inch, oi*inch, "6")
            c.drawString(7.88*inch, oi*inch, "6")
            oi -= oy

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 8.53*inch, "V. HEALTH AND MENTAL HEALTH")
        c.setFont("Times-Roman", 7.5, leading=None)
        c.drawString(0.3*inch, 8.38*inch, "Absence of Adequate Health Services")
        c.drawString(0.3*inch, 8.24*inch, "Inaccessibility of Health Services")
        c.drawString(0.3*inch, 8.09*inch, "Absence of Support Services Needed to Use Health")
        c.drawString(0.3*inch, 7.94*inch, "Absence of Adequate Mental Health Services")
        c.drawString(0.3*inch, 7.79*inch, "Inaccessibility of Mental Health Services")
        c.drawString(0.3*inch, 7.64*inch, "Absence of Support Services Needed to Use Mental Health Services")
        c.drawString(0.3*inch, 7.49*inch, "Others (specify)")

        c.setFillColor(black)
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(4.1*inch, 0.45*inch,"Page 2")
        c.saveState()
        create_header(c, None)
        create_footer(c,None)
        c.restoreState()
        c.showPage()



    if page3 == 3:
        c.setStrokeColor(black)
        c.setLineWidth(1)# horizontalline top
        c.line(0.25*inch,10.45*inch,8*inch,10.45*inch)

        c.setLineWidth(1)# horizontalline bottom
        c.line(0.25*inch,1.7*inch,8*inch,1.7*inch)

        c.setLineWidth(1)# verticalline left
        c.line(0.25*inch,1.7*inch,0.25*inch,10.45*inch)

        c.setLineWidth(1)# verticalline right
        c.line(8*inch,1.7*inch,8*inch,10.45*inch)

        c.setFillColor(white)
        c.rect(0.25*inch,9.25*inch,7.75*inch,1.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 7.7, leading=None)
        c.drawString(0.3*inch, 10.33*inch, "IV. PROBLEMS IN THE ENVIRONMENT")
        c.drawString(0.3*inch, 10.2*inch, "A. ECONOMIC BASIC NEEDS SYSTEMS PROBLEMS")

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(3.1*inch, 10.33*inch, "SEVERITY INDEX")
        c.drawString(3.1*inch, 10.15*inch, "1. No problem")
        c.drawString(3.1*inch, 10*inch, "2. Low")
        c.drawString(3.1*inch, 9.85*inch, "3. Moderate")
        c.drawString(3.1*inch, 9.7*inch, "4. High")
        c.drawString(3.1*inch, 9.55*inch, "5. Very High")
        c.drawString(3.1*inch, 9.4*inch, "6. Catastrophic")

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(5.5*inch, 10.33*inch, "DURATION INDEX")
        c.drawString(5.5*inch, 10.15*inch, "1. More than five years")
        c.drawString(5.5*inch, 10*inch, "2. One to five years")
        c.drawString(5.5*inch, 9.85*inch, "3. Six mos. to one year")
        c.drawString(5.5*inch, 9.7*inch, "4. One to six mos.")
        c.drawString(5.5*inch, 9.55*inch, "5. Two weeks to one month")
        c.drawString(5.5*inch, 9.4*inch, "6. Less than two weeks")


        
        c.setFillColor(white)
        c.rect(0.25*inch,8.85*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,8.65*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,8.45*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,8.25*inch,7.75*inch,0.2*inch,fill=1)
        
        c.setFillColor(white)
        c.rect(0.25*inch,7.85*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,7.65*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,7.45*inch,7.75*inch,0.2*inch,fill=1)
        
        c.setFillColor(white)
        c.rect(0.25*inch,7.05*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,6.85*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,6.65*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,6.45*inch,7.75*inch,0.2*inch,fill=1)
        
        c.setFillColor(white)
        c.rect(0.25*inch,6.05*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,5.85*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,5.65*inch,7.75*inch,0.2*inch,fill=1)
        
        c.setFillColor(white)
        c.rect(0.25*inch,5.25*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,5.05*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,4.85*inch,7.75*inch,0.2*inch,fill=1)
       
        c.setFillColor(white)
        c.rect(0.25*inch,4.45*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,4.25*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,4.05*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor(white)
        c.rect(0.25*inch,3.85*inch,7.75*inch,0.2*inch,fill=1)

        c.setFillColor(skyblue)
        c.rect(0.25*inch,3.6*inch,7.75*inch,0.25*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 3.66*inch, "ASSESSMENT FINDINGS")
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(4.2*inch, 3.66*inch, "RECOMMENDED INTERVENTIONS")

        c.setLineWidth(1)# verticalline right
        c.line(3*inch,3.85*inch,3*inch,10.45*inch)
        c.line(3.39*inch,3.85*inch,3.39*inch,9.05*inch)
        c.line(3.78*inch,3.85*inch,3.78*inch,9.05*inch)
        c.line(4.18*inch,1.7*inch,4.18*inch,9.05*inch)#
        c.line(4.56*inch,3.85*inch,4.56*inch,9.05*inch)
        c.line(4.96*inch,3.85*inch,4.96*inch,9.05*inch)

        c.line(5.375*inch,3.85*inch,5.375*inch,10.45*inch)
        c.line(5.8*inch,3.85*inch,5.78*inch,9.05*inch)
        c.line(6.24*inch,3.85*inch,6.24*inch,9.05*inch)
        c.line(6.7*inch,3.85*inch,6.7*inch,9.05*inch)
        c.line(7.15*inch,3.85*inch,7.15*inch,9.05*inch)
        c.line(7.6*inch,3.85*inch,7.6*inch,9.05*inch)

        c.setFillColor(white)
        c.rect(0.25*inch,9.05*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 9.1*inch, "1. FOOD NUTRITION")
        c.drawString(0.3*inch, 8.9*inch, "Lack of regular food supply")
        c.drawString(0.3*inch, 8.7*inch, "Nutritionally Inadequate  food supply")
        c.drawString(0.3*inch, 8.5*inch, "Documented Malnutrition")
        c.drawString(0.3*inch, 8.3*inch, "Others (specify)")
        c.setFillColor(white)
        c.rect(0.25*inch,8.05*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 8.1*inch, "2. SHELTER")
        c.drawString(0.3*inch, 7.9*inch, "Absence of Shelter")
        c.drawString(0.3*inch, 7.7*inch, "Substandard or inadequate shelter")
        c.drawString(0.3*inch, 7.5*inch, "Other (specify)")
        c.setFillColor(white)
        c.rect(0.25*inch,7.25*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 7.3*inch, "3. EMPLOYMENT")
        c.setFont("Times-Roman", 6.5, leading=None)
        c.drawString(0.3*inch, 7.1*inch, "Unemployment, Employment is not available in the community")
        c.drawString(0.3*inch, 6.9*inch, "Underemployment , adequate employment not available in the community")
        c.drawString(0.3*inch, 6.75*inch, "Inappropriate employment, lack of socially/legally  acceptable")
        c.drawString(0.3*inch, 6.68*inch, "employment in the community")
        c.drawString(0.3*inch, 6.5*inch, "Other (specify)")
        c.setFillColor(white)
        c.rect(0.25*inch,6.25*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 6.3*inch, "4. ECONOMIC RESOURCES")
        c.drawString(0.3*inch, 6.1*inch, "Insufficient community resources for basic sustenance")
        c.drawString(0.3*inch, 5.95*inch, "Insufficient resources in the community to")
        c.drawString(0.3*inch, 5.88*inch, "provide for needed services beyond")
        c.drawString(0.3*inch, 5.7*inch, "Others(specify)")
        c.setFillColor(white)
        c.rect(0.25*inch,5.45*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 5.5*inch, "5. TRANSPORTATION")
        c.drawString(0.3*inch, 5.3*inch, "No personal/public transportation to job/needed services")
        c.drawString(0.3*inch, 5.1*inch, "Others(specify)")
        c.setFillColor(white)
        c.rect(0.25*inch,4.65*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 4.7*inch, "B.  AFFECTIONAL SUPPORT SYSTEM")

        c.setFillColor(white)
        c.rect(0.25*inch,4.85*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 4.9*inch, "NO PROBLEMS IN ECONOMIC/BASIC NEEDS")
        c.drawString(0.3*inch, 4.5*inch, "Absence of affectional support system")
        c.drawString(0.3*inch, 4.3*inch, "Support system inadequate to meet affectional needs")
        c.drawString(0.3*inch, 4.1*inch, "Excessively involved support system")
        c.drawString(0.3*inch, 3.9*inch, "Others(specify)")

        ex = 0.2  
        ew= 8.9
        for re in range(4):
            c.setFillColor("black")
            c.setFont("Times-Bold", 10, leading=None)
            c.drawString(3.15*inch, ew*inch, "1")
            c.drawString(3.55*inch, ew*inch, "2")
            c.drawString(3.95*inch, ew*inch, "3")
            c.drawString(4.35*inch, ew*inch, "4")
            c.drawString(4.75*inch, ew*inch, "5")
            c.drawString(5.15*inch, ew*inch, "6")
            c.drawString(5.55*inch, ew*inch, "1")
            c.drawString(5.95*inch, ew*inch, "2")
            c.drawString(6.45*inch, ew*inch, "3")
            c.drawString(6.85*inch, ew*inch, "4")
            c.drawString(7.35*inch, ew*inch, "5")
            c.drawString(7.75*inch, ew*inch, "6")
            ew -= ex

        eu = 0.2  
        ea= 7.9
        for re in range(3):
            c.setFillColor("black")
            c.setFont("Times-Bold", 10, leading=None)
            c.drawString(3.15*inch, ea*inch, "1")
            c.drawString(3.55*inch, ea*inch, "2")
            c.drawString(3.95*inch, ea*inch, "3")
            c.drawString(4.35*inch, ea*inch, "4")
            c.drawString(4.75*inch, ea*inch, "5")
            c.drawString(5.15*inch, ea*inch, "6")
            c.drawString(5.55*inch, ea*inch, "1")
            c.drawString(5.95*inch, ea*inch, "2")
            c.drawString(6.45*inch, ea*inch, "3")
            c.drawString(6.85*inch, ea*inch, "4")
            c.drawString(7.35*inch, ea*inch, "5")
            c.drawString(7.75*inch, ea*inch, "6")
            ea -= eu

        eqq = 0.2  
        eaa= 7.1
        for re in range(4):
            c.setFillColor("black")
            c.setFont("Times-Bold", 10, leading=None)
            c.drawString(3.15*inch, eaa*inch, "1")
            c.drawString(3.55*inch, eaa*inch, "2")
            c.drawString(3.95*inch, eaa*inch, "3")
            c.drawString(4.35*inch, eaa*inch, "4")
            c.drawString(4.75*inch, eaa*inch, "5")
            c.drawString(5.15*inch, eaa*inch, "6")
            c.drawString(5.55*inch, eaa*inch, "1")
            c.drawString(5.95*inch, eaa*inch, "2")
            c.drawString(6.45*inch, eaa*inch, "3")
            c.drawString(6.85*inch, eaa*inch, "4")
            c.drawString(7.35*inch, eaa*inch, "5")
            c.drawString(7.75*inch, eaa*inch, "6")
            eaa -= eqq
        qqa = 0.2  
        qwe= 6.1
        for re in range(3):
            c.setFillColor("black")
            c.setFont("Times-Bold", 10, leading=None)
            c.drawString(3.15*inch, qwe*inch, "1")
            c.drawString(3.55*inch, qwe*inch, "2")
            c.drawString(3.95*inch, qwe*inch, "3")
            c.drawString(4.35*inch, qwe*inch, "4")
            c.drawString(4.75*inch, qwe*inch, "5")
            c.drawString(5.15*inch, qwe*inch, "6")
            c.drawString(5.55*inch, qwe*inch, "1")
            c.drawString(5.95*inch, qwe*inch, "2")
            c.drawString(6.45*inch, qwe*inch, "3")
            c.drawString(6.85*inch, qwe*inch, "4")
            c.drawString(7.35*inch, qwe*inch, "5")
            c.drawString(7.75*inch, qwe*inch, "6")
            qwe -= qqa
        wqa = 0.2  
        wwe= 5.3
        for re in range(2):
            c.setFillColor("black")
            c.setFont("Times-Bold", 10, leading=None)
            c.drawString(3.15*inch, wwe*inch, "1")
            c.drawString(3.55*inch, wwe*inch, "2")
            c.drawString(3.95*inch, wwe*inch, "3")
            c.drawString(4.35*inch, wwe*inch, "4")
            c.drawString(4.75*inch, wwe*inch, "5")
            c.drawString(5.15*inch, wwe*inch, "6")
            c.drawString(5.55*inch, wwe*inch, "1")
            c.drawString(5.95*inch, wwe*inch, "2")
            c.drawString(6.45*inch, wwe*inch, "3")
            c.drawString(6.85*inch, wwe*inch, "4")
            c.drawString(7.35*inch, wwe*inch, "5")
            c.drawString(7.75*inch, wwe*inch, "6")
            wwe -= wqa
        yye = 0.2  
        yyq= 4.5
        for re in range(4):
            c.setFillColor("black")
            c.setFont("Times-Bold", 10, leading=None)
            c.drawString(3.15*inch, yyq*inch, "1")
            c.drawString(3.55*inch, yyq*inch, "2")
            c.drawString(3.95*inch, yyq*inch, "3")
            c.drawString(4.35*inch, yyq*inch, "4")
            c.drawString(4.75*inch, yyq*inch, "5")
            c.drawString(5.15*inch, yyq*inch, "6")
            c.drawString(5.55*inch, yyq*inch, "1")
            c.drawString(5.95*inch, yyq*inch, "2")
            c.drawString(6.45*inch, yyq*inch, "3")
            c.drawString(6.85*inch, yyq*inch, "4")
            c.drawString(7.35*inch, yyq*inch, "5")
            c.drawString(7.75*inch, yyq*inch, "6")
            yyq -= yye

        swa_desc = SWA.objects.filter(uis = uis)
        for sw in swa_desc:
            desc_swa = sw.swa_desc
            p = Paragraph(desc_swa, style=custom_font_size_swa )
            p.wrapOn(c, 280,20)  
            p.drawOn(c,0.3*inch,1.8*inch) 
            p.wrapOn(c, 275,20) 
            p.drawOn(c,4.2*inch,1.8*inch) 

        c.setFillColor(black)
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.3*inch, 1.5*inch,"Ako si                                                                             , nagsasabing naiintindihan ko na nag pag hingi namin ng tulong sa Medical Social Service ay naayon sa kinalabasan ng Interview ng Social")
        c.drawString(0.3*inch, 1.4*inch,"Worker sa amin. Anumang maling impormasyon na ibinigay namin ay pwedeng dahilan para mapawalang bisa ang aming hinihinging tulong. Nang dahil dito, babayaran namin lahat ng bill ng")
        c.drawString(0.3*inch, 1.3*inch,"aming pasyente dito sa hospital.")
        c.drawString(0.6*inch, 1.5*inch, informant_fullname)


        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.7*inch, 1*inch, "____________________________________________________________")
        uw = c.stringWidth("Patient's Signature")/100
        uiw = 210/100
        cu = (uiw - uw) / 2
        fxi = cu + 0.95
        c.drawString(fxi*inch, 0.9*inch, "Patient's Signature" )

        c.drawString(4.7*inch, 1*inch, "____________________________________________________________")

        uwp = c.stringWidth(request.session['position'])/100
        uiwp = 210/100
        cup = (uiwp - uwp) / 2
        fxip = cup + 4.55
        c.drawString(fxip*inch, 0.9*inch,"License No.:"  )

        uwn = c.stringWidth(request.session['name'])/100
        uiwn = 210/100
        cun = (uiwn - uwn) / 2
        fxin = cun + 4.95
        c.drawString(fxin*inch, 1.02*inch, request.session['name'] )

        c.setFillColor(black)
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(4.1*inch, 0.45*inch,"Page 3")
        c.saveState()
        create_header(c, None)
        create_footer(c,None)
        c.restoreState()
        c.showPage()
    
    c.save()
    pdf = buf.getvalue()
    buf.close()
    response.write(pdf)
    return response
