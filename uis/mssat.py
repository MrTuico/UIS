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
    c.setStrokeColorRGB(0, 0, 1)  # Blue color
    c.setLineWidth(2)
    c.line(0.25*inch,10.55*inch,8*inch,10.55*inch)
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

def mssat_pdf(request,uis):
    
    page1 = 1
    page2 = 2
    page3 = 3
    if page1 == 1:
        buf = io.BytesIO()
        c = canvas.Canvas(buf)
        response = HttpResponse(content_type='application/pdf')
        c.setTitle("MEDICAL SOCIAL SERVICE ASSESSMENT TOOL")
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
    
        c.setFillColor(white)#single
        c.rect(0.25*inch,10.15*inch,7.75*inch,0.3*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 15, leading=None)
        c.drawString(2.4*inch, 10.2*inch, "Medical Social Service Assessment Tool")

        c.setFillColor(white)#1
        c.rect(0.25*inch,9.65*inch,1.5*inch,0.5*inch,fill=1)
        c.rect(1.75*inch,9.65*inch,3*inch,0.5*inch,fill=1)
        c.rect(4.75*inch,9.65*inch,0.5*inch,0.5*inch,fill=1)
        c.rect(4.75*inch,9.65*inch,0.5*inch,0.2*inch,fill=1)
        c.rect(5.25*inch,9.65*inch,0.5*inch,0.5*inch,fill=1)
        c.rect(5.25*inch,9.65*inch,0.5*inch,0.2*inch,fill=1)
        c.rect(5.75*inch,9.65*inch,1.125*inch,0.5*inch,fill=1)
        c.rect(6.875*inch,9.65*inch,1.125*inch,0.5*inch,fill=1)

        

        get_details = UIS.objects.filter(uis = uis)
        for i in get_details:
            hospno = i.hospno
            hsize_f = float(i.householdsize)
            hsize = i.householdsize
            tot_income_f = float(i.total_income)
            tot_income = i.total_income
            tot_expense = float(i.total_expense)
            per_capita_income = tot_income_f/hsize_f
            c.setFillColor("black")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(5.85*inch, 9.8*inch, hospno)
        informant_details = Informant.objects.filter(uis = uis)
        for a in informant_details:
            doi_init = a.date_of_intake
            date_conv = datetime.strptime(doi_init, '%Y-%m-%d')
            doi = date_conv.strftime('%B %d, %Y')
            informant_fullname = a.fullname
            informant_address = a.address
            informant_time_of_interview = a.time_of_interview
            informant_relation_to_patient = a.relation_to_patient
            informant_contact_number = a.contact_number
            c.setFillColor("black")
            c.setFont("Times-Bold", 9, leading=None)
            c.drawString(0.4*inch, 9.8*inch, doi)

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
            phil_mem = sc.phil_mem
            mswd = sc.mswd_cassif
            employer = sc.employer
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
            c.drawString(2*inch, 9.8*inch, doac)
            c.drawString(4.8*inch, 9.72*inch, sc.basic_ward)
            c.drawString(5.3*inch, 9.72*inch, sc.non_basic)
            c.drawString(6.93*inch, 9.8*inch, sc.mss_no)
            
            
            

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.28*inch, 10.05*inch, "DATE OF INTERVIEW:")
        c.drawString(1.78*inch, 10.05*inch, "DATE OF ADMISSION/CONSULTATION:")
        c.drawString(4.77*inch, 10.05*inch, "Basic ward")
        c.drawString(4.8*inch, 9.95*inch, "(specify)")
        c.drawString(5.27*inch, 10.05*inch, "Non basic")
        c.drawString(5.3*inch, 9.95*inch, "(specify)")
        c.drawString(5.78*inch, 10.05*inch, "HOSPITAL NUMBER:")
        c.drawString(6.9*inch, 10.05*inch, "MSS NO:")

        c.setFillColor(white)#2
        c.rect(0.25*inch,9.35*inch,2*inch,0.3*inch,fill=1)
        c.rect(2.25*inch,9.35*inch,4*inch,0.3*inch,fill=1)
        c.rect(6.25*inch,9.35*inch,1.75*inch,0.3*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.3*inch, 9.39*inch, src_referal_name)
        c.drawString(2.3*inch, 9.39*inch, src_address)
        c.drawString(6.3*inch, 9.39*inch, src_cnum)

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.28*inch, 9.55*inch, "SOURCE OF REFERRAL NAME:")
        c.drawString(2.28*inch, 9.55*inch, "ADDRESS:")
        c.drawString(6.28*inch, 9.55*inch, "Contact Number:")

        c.setFillColor(white)#3
        c.rect(0.25*inch,9.05*inch,2*inch,0.3*inch,fill=1)
        c.rect(2.25*inch,9.05*inch,4*inch,0.3*inch,fill=1)
        c.rect(6.25*inch,9.05*inch,1.75*inch,0.3*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.28*inch, 9.25*inch, "Informant:")
        c.drawString(2.28*inch, 9.25*inch, "Relation to patient")
        c.drawString(6.28*inch, 9.25*inch, "Contact Number:")

        c.setFillColor("black")
        c.setFont("Times-Bold", 6.5, leading=None)
        c.drawString(0.3*inch, 9.1*inch, informant_fullname)
        c.drawString(2.3*inch, 9.1*inch, informant_relation_to_patient)
        c.drawString(6.3*inch, 9.1*inch, informant_contact_number)

        c.setFillColor(skyblue)#4
        c.rect(0.25*inch,8.9*inch,7.75*inch,0.15*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.28*inch, 8.95*inch, "DEMOPGRAPHIC DATA:")

        c.setFillColor(white)#5
        c.rect(0.25*inch,8.75*inch,6*inch,0.15*inch,fill=1)
        c.rect(6.25*inch,8.75*inch,0.3*inch,0.15*inch,fill=1)
        c.rect(6.55*inch,8.75*inch,0.3*inch,0.15*inch,fill=1)
        c.rect(6.85*inch,8.75*inch,1.15*inch,0.15*inch,fill=1)
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
        c.drawString(2.9*inch, 8.8*inch, "Patient's Name")
        c.drawString(6.28*inch, 8.8*inch, "Age")
        c.drawString(6.58*inch, 8.8*inch, "Sex")
        c.drawString(7.25*inch, 8.8*inch, "Gender")
        


        c.setFillColor(white)#6
        c.rect(0.25*inch,8.6*inch,2*inch,0.15*inch,fill=1)
        c.rect(2.25*inch,8.6*inch,2*inch,0.15*inch,fill=1)
        c.rect(4.25*inch,8.6*inch,2*inch,0.15*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(1*inch, 8.64*inch, "Surname")
        c.drawString(3.1*inch, 8.64*inch, "First")
        c.drawString(5.15*inch, 8.64*inch, "Last")

        c.setFillColor(white)#7
        c.rect(0.25*inch,8.4*inch,6*inch,0.2*inch,fill=1)
    
        uw = c.stringWidth(ii_cname)/100
        uiw = 432/100
        cu = (uiw - uw) / 2
        fxi = cu + 0.55
        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(fxi*inch, 8.44*inch, ii_cname)
        c.drawString(6.3*inch, 8.44*inch, ii_age)
    

        c.setFillColor(white)
        c.rect(6.25*inch,8.4*inch,0.3*inch,0.35*inch,fill=1)
        c.rect(6.55*inch,8.4*inch,0.3*inch,0.35*inch,fill=1)
        c.rect(6.85*inch,8.4*inch,0.3*inch,0.35*inch,fill=1)
        c.rect(7.15*inch,8.4*inch,0.3*inch,0.35*inch,fill=1)
        c.rect(7.45*inch,8.4*inch,0.55*inch,0.35*inch,fill=1)

        c.setLineWidth(1)
        if ii_gender == 'MALE':
            c.setFillColor(black)
            c.rect(6.95*inch,8.45*inch,0.09*inch,0.09*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(6.95*inch,8.45*inch,0.09*inch,0.09*inch,fill=1)
        if ii_gender == "FEMALE":
            c.setFillColor(black)
            c.rect(7.25*inch,8.45*inch,0.09*inch,0.09*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(7.25*inch,8.45*inch,0.09*inch,0.09*inch,fill=1)
        if ii_gender != 'MALE' and ii_gender != 'FEMALE':
            c.setFillColor(black)
            c.rect(7.66*inch,8.45*inch,0.09*inch,0.09*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(7.66*inch,8.45*inch,0.09*inch,0.09*inch,fill=1)
        
        
        

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(6.95*inch, 8.57*inch, "M")
        c.drawString(7.25*inch, 8.57*inch, "F")
        c.drawString(7.57*inch, 8.57*inch, "LGBT")

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(6.3*inch, 8.44*inch, ii_age)
        if ii_gender == 'FEMALE':
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(6.65*inch, 8.44*inch, "F")
        elif ii_gender == "MALE":
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(6.65*inch, 8.44*inch, "M")
        else:
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(6.65*inch, 8.44*inch, "N/A")
            

        

        c.setFillColor(white)#8
        c.rect(0.25*inch,8.25*inch,1.5*inch,0.15*inch,fill=1)
        c.rect(1.75*inch,8.25*inch,1.5*inch,0.15*inch,fill=1)
        c.rect(3.25*inch,8.25*inch,3.5*inch,0.15*inch,fill=1)
        c.rect(6.75*inch,8.25*inch,1.25*inch,0.15*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.65*inch, 8.29*inch, "Date of Birth")
        c.drawString(2.2*inch, 8.29*inch, "Place of Birth")
        c.drawString(4.64*inch, 8.29*inch, "Civil Status")
        
        c.drawString(7.15*inch, 8.29*inch, "Religion")

        c.setFillColor(white)#9
        c.rect(0.25*inch,8.05*inch,1.5*inch,0.2*inch,fill=1)
        c.rect(1.75*inch,8.05*inch,1.5*inch,0.2*inch,fill=1)
        c.rect(3.25*inch,8.05*inch,3.5*inch,0.2*inch,fill=1)
        c.rect(6.75*inch,8.05*inch,1.25*inch,0.2*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.5*inch, 8.1*inch, ii_dob)
        c.setFont("Times-Bold", 6.5, leading=None)
        c.drawString(1.8*inch, 8.1*inch, ii_pob)
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(6.8*inch, 8.1*inch, ii_rel)

        c.setLineWidth(1)
        if ii_cstat == 'SINGLE':
            c.setFillColor(black)
            c.rect(3.35*inch,8.1*inch,0.09*inch,0.09*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(3.35*inch,8.1*inch,0.09*inch,0.09*inch,fill=1)
        c.setFillColor(white)
        c.rect(3.9*inch,8.1*inch,0.09*inch,0.09*inch,fill=1)
        if ii_cstat == 'MARRIED':
            c.setFillColor(black)
            c.rect(4.7*inch,8.1*inch,0.09*inch,0.09*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(4.7*inch,8.1*inch,0.09*inch,0.09*inch,fill=1)
        if ii_cstat == 'DIVORSED':
            c.setFillColor(black)
            c.rect(5.3*inch,8.1*inch,0.09*inch,0.09*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(5.3*inch,8.1*inch,0.09*inch,0.09*inch,fill=1)
        if ii_cstat == 'SEPARATED':
            c.setFillColor(black)
            c.rect(6.1*inch,8.1*inch,0.09*inch,0.09*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(6.1*inch,8.1*inch,0.09*inch,0.09*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(3.47*inch, 8.12*inch, "Single")
        c.drawString(4*inch, 8.12*inch, "Common Law")
        c.drawString(4.8*inch, 8.12*inch, "Married")
        c.drawString(5.4*inch, 8.12*inch, "Sep d'facto")
        c.drawString(6.2*inch, 8.12*inch, "Sep Legal")

    

        c.setFillColor(white)#10
        c.rect(0.25*inch,7.9*inch,2.55*inch,0.15*inch,fill=1)
        c.rect(2.8*inch,7.9*inch,2.55*inch,0.15*inch,fill=1)
        c.rect(5.35*inch,7.9*inch,2.65*inch,0.15*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(1*inch, 7.95*inch, "Permannent Address")
        c.drawString(3.5*inch, 7.95*inch, "TEMPORARY ADDRESS")
        c.drawString(6*inch, 7.95*inch, "Type of Living Arrangement")

        

        c.setFillColor(white)#11
        c.rect(0.25*inch,7.6*inch,2.55*inch,0.3*inch,fill=1)
        c.rect(2.8*inch,7.6*inch,2.55*inch,0.3*inch,fill=1)

        c.setFillColor(white)#11
        c.rect(5.35*inch,7.8*inch,0.4*inch,0.1*inch,fill=1)
        c.rect(5.35*inch,7.6*inch,0.4*inch,0.2*inch,fill=1)

        c.setFillColor(white)#11
        c.rect(5.75*inch,7.8*inch,0.4*inch,0.1*inch,fill=1)
        c.rect(5.75*inch,7.6*inch,0.4*inch,0.2*inch,fill=1)

        c.rect(6.15*inch,7.8*inch,0.4*inch,0.1*inch,fill=1)
        c.rect(6.15*inch,7.6*inch,0.4*inch,0.2*inch,fill=1)

        c.rect(6.55*inch,7.8*inch,0.4*inch,0.1*inch,fill=1)
        c.rect(6.55*inch,7.6*inch,0.4*inch,0.2*inch,fill=1)

        c.rect(6.95*inch,7.8*inch,0.4*inch,0.1*inch,fill=1)
        c.rect(6.95*inch,7.6*inch,0.4*inch,0.2*inch,fill=1)

        c.rect(7.35*inch,7.8*inch,0.65*inch,0.1*inch,fill=1)
        c.rect(7.35*inch,7.6*inch,0.65*inch,0.2*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Bold", 12, leading=None)
        if tla == 'OWNED':
            c.drawString(5.5*inch, 7.64*inch, "/")
        elif tla == 'RENT':
            c.drawString(5.9*inch, 7.64*inch, "/")
        elif tla == 'SHARED':
            c.drawString(6.3*inch, 7.64*inch, "/")
        elif tla == 'PRIVATE':
            c.drawString(6.7*inch, 7.64*inch, "/")
        elif tla == 'INSTITUTION':
            c.drawString(7.15*inch, 7.64*inch, "/")
        elif tla == 'HOMELESS':
            c.drawString(7.65*inch, 7.64*inch, "/")
        else:
            c.drawString(5.5*inch, 7.64*inch, "")

        p = Paragraph(ii_perma, style=custom_font_size )
        p.wrapOn(c, 175,20)  
        p.drawOn(c,0.3*inch,7.65*inch) 

        p = Paragraph(ii_pra, style=custom_font_size )
        p.wrapOn(c, 175,20)  
        p.drawOn(c,2.85*inch,7.65*inch) 

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(5.39*inch, 7.82*inch, "Owned")
        c.drawString(5.8*inch, 7.82*inch, "Rent")
        c.drawString(6.17*inch, 7.82*inch, "Shared")
        c.drawString(6.56*inch, 7.82*inch, "Private")
        c.drawString(6.95*inch, 7.82*inch, "Institution")
        c.drawString(7.5*inch, 7.82*inch, "Homeless")


        c.setFillColor(white)#12
        c.rect(0.25*inch,7.35*inch,1.2*inch,0.25*inch,fill=1)
        c.rect(1.45*inch,7.35*inch,1.2*inch,0.25*inch,fill=1)
        c.rect(2.65*inch,7.35*inch,2*inch,0.25*inch,fill=1)
        c.rect(4.65*inch,7.35*inch,0.5*inch,0.25*inch,fill=1)
        c.rect(5.15*inch,7.35*inch,1.425*inch,0.25*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 7.43*inch, "Educational Attainment")
        c.drawString(1.75*inch, 7.43*inch, "Occupation")
        c.drawString(3.4*inch, 7.43*inch, "Employer")
        c.drawString(4.7*inch, 7.43*inch, "Income")
        c.drawString(5.2*inch, 7.43*inch, "Philhealth Membership")
        c.drawString(6.75*inch, 7.5*inch, "MSWD Classification")

    

        c.setLineWidth(1)
        if mswd == 'FINANCIALLY CAPABLE':
            c.setFillColor(black)
            c.rect(6.65*inch,7.35*inch,0.09*inch,0.09*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(6.65*inch,7.35*inch,0.09*inch,0.09*inch,fill=1)
        if mswd == 'FINANCIALLY INCAPABLE':
            c.setFillColor(black)
            c.rect(6.65*inch,7.2*inch,0.09*inch,0.09*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(6.65*inch,7.2*inch,0.09*inch,0.09*inch,fill=1) 
        

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(6.78*inch, 7.35*inch, "Financially Incapable")
        c.drawString(6.78*inch, 7.2*inch, "Financially Capable")

        c.setFillColor(white)#13
        c.rect(0.25*inch,7.15*inch,1.2*inch,0.2*inch,fill=1)
        c.rect(1.45*inch,7.15*inch,1.2*inch,0.2*inch,fill=1)
        c.rect(2.65*inch,7.15*inch,2*inch,0.2*inch,fill=1)
        c.rect(4.65*inch,7.15*inch,0.5*inch,0.2*inch,fill=1)
        c.rect(5.15*inch,7.15*inch,1.425*inch,0.2*inch,fill=1)

        c.setLineWidth(1)
        if phil_mem == 'DIRECT':
            c.setFillColor(black)
            c.rect(5.2*inch,7.2*inch,0.09*inch,0.09*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(5.2*inch,7.2*inch,0.09*inch,0.09*inch,fill=1)
        if phil_mem == 'INDIRECT':
            c.setFillColor(white)
            c.rect(5.8*inch,7.2*inch,0.09*inch,0.09*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(5.8*inch,7.2*inch,0.09*inch,0.09*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(5.32*inch, 7.2*inch, "DIRECT")
        c.drawString(5.92*inch, 7.2*inch, "INDIRECT")

    

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(0.3*inch, 7.17*inch, ii_hea)
        c.drawString(4.67*inch, 7.17*inch, ii_mi)
        
        p = Paragraph(employer, style=custom_font_size )
        p.wrapOn(c, 150,20)  
        p.drawOn(c,2.67*inch,7.17*inch) 

        p = Paragraph(ii_occu, style=custom_font_size )
        p.wrapOn(c, 85,20)  
        p.drawOn(c,1.47*inch,7.17*inch) 
        scsr = SCSR.objects.filter(uis = uis)
        for sc in scsr:
            employer =sc.employer
            p = Paragraph(employer, style=custom_font_size )
            p.wrapOn(c, 130,20)  
            p.drawOn(c,2.67*inch,7.17*inch) 

        c.setFillColor(white)#14
        c.rect(0.25*inch,7*inch,7.75*inch,0.15*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(3.2*inch, 7.02*inch, "Marginalized Sectorial Membeship")

        c.setFillColor(white)#15
        c.rect(0.25*inch,6*inch,0.775*inch,1*inch,fill=1)

        if marginalized_sec_mem == 'ARTISANAL FISHERFOLK':
            c.setFillColor(black)
            c.rect(0.55*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(0.55*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)

        c.setFillColor(white)    
        c.rect(1.025*inch,6*inch,0.775*inch,1*inch,fill=1)

        if marginalized_sec_mem == 'FARMERS AND LANDLESS RURAL WORKERS':
            c.setFillColor(black)
            c.rect(1.325*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(1.325*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)

        c.setFillColor(white) 
        c.rect(1.8*inch,6*inch,0.775*inch,1*inch,fill=1)
        
        if marginalized_sec_mem == 'INDIGENOUS PEOPLE':
            c.setFillColor(black)
            c.rect(2.1*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(2.1*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)

        c.setFillColor(white) 
        c.rect(2.575*inch,6*inch,0.775*inch,1*inch,fill=1)
        
        if marginalized_sec_mem == 'FORMAL AND LABOR MIGRANT WORKERS':
            c.setFillColor(black)
            c.rect(2.875*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(2.875*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)

        c.setFillColor(white)
        c.rect(3.35*inch,6*inch,0.775*inch,1*inch,fill=1)

        if marginalized_sec_mem == 'WORKERS IN INFORMAL SECTORS':
            c.setFillColor(black)
            c.rect(3.65*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(3.65*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)

        c.setFillColor(white)
        c.rect(4.125*inch,6*inch,0.775*inch,1*inch,fill=1)
        
        if marginalized_sec_mem == 'SENIOR CITIZEN':
            c.setFillColor(black)
            c.rect(4.425*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(4.425*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)

        c.setFillColor(white)
        c.rect(4.9*inch,6*inch,0.775*inch,1*inch,fill=1)
    
        if marginalized_sec_mem == 'PWD':
            c.setFillColor(black)
            c.rect(5.2*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(5.2*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)

        c.setFillColor(white)
        c.rect(5.675*inch,6*inch,0.775*inch,1*inch,fill=1)

        if marginalized_sec_mem == 'VICTIMS OF DISASTERS AND CALAMTIES':
            c.setFillColor(black)
            c.rect(5.975*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(5.975*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)

        c.setFillColor(white)
        c.rect(6.45*inch,6*inch,0.775*inch,1*inch,fill=1)
        
        if marginalized_sec_mem == 'URBAN POOR':
            c.setFillColor(black)
            c.rect(6.75*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(6.75*inch,6.1*inch,0.15*inch,0.15*inch,fill=1)
        c.setFillColor(white)
        c.rect(7.225*inch,6*inch,0.775*inch,1*inch,fill=1)
        c.rect(7.225*inch,6.85*inch,0.775*inch,0.15*inch,fill=1)

        if marginalized_sec_mem == 'OTHERS':
            c.setFillColor(black)
            c.rect(7.3*inch,6.87*inch,0.1*inch,0.1*inch,fill=1)
        else:
            c.setFillColor(white)
            c.rect(7.3*inch,6.87*inch,0.1*inch,0.1*inch,fill=1)

        

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.45*inch, 6.8*inch, "Artisanal")
        c.drawString(0.42*inch, 6.65*inch, "Fisherfolk")

        c.drawString(1.1*inch, 6.8*inch, "Farmer and ")
        c.drawString(1.1*inch, 6.65*inch, "Landless Rural")
        c.drawString(1.1*inch, 6.5*inch, "Workers")

        c.drawString(1.92*inch, 6.8*inch, "Indigenous")
        c.drawString(2*inch, 6.65*inch, "People")

        c.drawString(2.67*inch, 6.8*inch, "Formal and")
        c.drawString(2.78*inch, 6.65*inch, "Labor")
        c.drawString(2.73*inch, 6.5*inch, "Migrant")
        c.drawString(2.72*inch, 6.35*inch, "Workers")

        c.drawString(3.5*inch, 6.8*inch, "Workers in")
        c.drawString(3.55*inch, 6.65*inch, "Informal")
        c.drawString(3.6*inch, 6.5*inch, "Sector")

        c.drawString(4.35*inch, 6.8*inch, "Señior")
        c.drawString(4.33*inch, 6.65*inch, "Citizen")

        c.drawString(5*inch, 6.8*inch, "Person with")
        c.drawString(5.05*inch, 6.65*inch, "Disability")

        c.drawString(5.85*inch, 6.8*inch, "Victims of")
        c.drawString(5.8*inch, 6.65*inch, "Disasters and")
        c.drawString(5.85*inch, 6.5*inch, "Calamities")

        c.drawString(6.58*inch, 6.65*inch, "Urban Poor")

        c.drawString(7.5*inch, 6.88*inch, "Others")
        c.drawString(7.25*inch, 6.74*inch, "(specify)")


        c.setFillColor(white)#16
        c.rect(0.25*inch,5.85*inch,7.75*inch,0.15*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(3.3*inch, 5.87*inch, "FAMILY COMPOSITIOM")

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(0.25*inch,5.65*inch,2.2*inch,0.2*inch,fill=1)
        c.rect(2.45*inch,5.65*inch,0.4*inch,0.2*inch,fill=1)
        c.rect(2.85*inch,5.65*inch,1*inch,0.2*inch,fill=1)
        c.rect(3.85*inch,5.65*inch,1*inch,0.2*inch,fill=1)
        c.rect(4.85*inch,5.65*inch,1*inch,0.2*inch,fill=1)
        c.rect(5.85*inch,5.65*inch,1*inch,0.2*inch,fill=1)
        c.rect(6.85*inch,5.65*inch,1.15*inch,0.2*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(1.21*inch, 5.7*inch, "NAME")
        c.drawString(2.5*inch, 5.7*inch, "AGE")
        c.drawString(2.95*inch, 5.7*inch, "CIVIL STATUS")
        c.drawString(6*inch, 5.7*inch, "OCCUPATION")
        c.drawString(6.9*inch, 5.7*inch, "MONTHLY INCOME")
        c.setFont("Times-Roman", 6.5, leading=None)
        c.drawString(3.86*inch, 5.7*inch, "RELATION TO PATIENT")
        c.drawString(5*inch, 5.77*inch, "EDUCATIONAL")
        c.drawString(5*inch, 5.68*inch, "ATTAINMENT")


        c.setLineWidth(1)
        c.setFillColor(white)

        a =0.15
        b = 5.5
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
        tt = 5.52
        for cc in famcom:
            c.setFillColor("black")
            c.setFont("Times-Bold", 6.5, leading=None)
            c.drawString(0.27*inch, tt *inch, cc.fullname)
            c.drawString(2.47*inch, tt *inch, cc.age)
            c.drawString(2.87*inch, tt *inch, cc.cstat)
            c.drawString(3.87*inch, tt *inch, cc.relation_to_patient)
            c.drawString(4.87*inch, tt *inch, cc.hea)
            c.drawString(5.87*inch, tt *inch, cc.occupation)
            famcom_mi = '{:,.2f}'.format(float(cc.mi))
            c.drawString(6.87*inch, tt *inch, famcom_mi)
            tt -=pp
        
        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(0.25*inch,4*inch,3.6*inch,0.15*inch,fill=1)

        c.rect(0.25*inch,3.85*inch,3.6*inch,0.15*inch,fill=1)
        c.rect(0.25*inch,3.7*inch,3.6*inch,0.15*inch,fill=1)
        c.rect(0.25*inch,3.55*inch,3.6*inch,0.15*inch,fill=1)

        xe = 0.15
        ye = 3.89
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
        c.drawString(0.5*inch, 4.05*inch, "OTHER SOURCES OF INCOME")
        c.drawString(3*inch, 4.05*inch, "AMOUNT")
        

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(3.85*inch,3.55*inch,1.2*inch,0.6*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(4.2*inch, 3.89*inch, hsize)
        c.setFillColor(white)
        c.rect(5.05*inch,3.35*inch,1.475*inch,0.8*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 7, leading=None)
        total_incomes = '{:,.2f}'.format(float(tot_income))
        c.drawString(5.5*inch, 3.89*inch, total_incomes)
        c.setFillColor(white)
        c.rect(6.525*inch,3.35*inch,1.475*inch,0.8*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 7, leading=None)
        total_pci = '{:,.2f}'.format(float(per_capita_income ))
        c.drawString(6.8*inch, 3.89*inch, total_pci)

        c.setFillColor("black")
        c.setFont("Times-Roman", 7, leading=None)
        c.drawString(3.9*inch, 4.05*inch, "Household Size:")
        c.drawString(5.1*inch, 4.05*inch, "Total Family Income:")
        c.drawString(6.55*inch, 4.05*inch, "Per Capita Income")

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(0.25*inch,3.35*inch,4.8*inch,0.2*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 9, leading=None)
        c.drawString(0.6*inch, 3.39*inch, "Sub Classification for OPD Patients")
        c.drawString(2.65*inch, 3.39*inch, "C1")
        c.drawString(3.65*inch, 3.39*inch, "C2")
        c.drawString(4.65*inch, 3.39*inch, "C3")
        c.setLineWidth(1)
        uis_id = UIS.objects.filter(uis=uis)
        for ud in uis_id:
            klass = ud.category
            if klass == 'C1':
                c.setFillColor(black)#SQUARES
                c.rect(2.5*inch,3.38*inch,0.12*inch,0.12*inch,fill=1)
            else:
                c.setFillColor(white)#SQUARES
                c.rect(2.5*inch,3.38*inch,0.12*inch,0.12*inch,fill=1)
            if klass == 'C2':
                c.setFillColor(black)#SQUARES
                c.rect(3.5*inch,3.38*inch,0.12*inch,0.12*inch,fill=1)
            else:
                c.setFillColor(white)#SQUARES
                c.rect(3.5*inch,3.38*inch,0.12*inch,0.12*inch,fill=1)
            if klass == 'C3':
                c.setFillColor(black)#SQUARES
                c.rect(4.5*inch,3.38*inch,0.12*inch,0.12*inch,fill=1)
            else:
                c.setFillColor(white)#SQUARES
                c.rect(4.5*inch,3.38*inch,0.12*inch,0.12*inch,fill=1)



        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(0.25*inch,2.35*inch,1.9375*inch,1*inch,fill=1)
        c.setLineWidth(1)
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
        if hauz == 'OWNED': #house
            c.setFillColor(black)
            c.rect(0.3*inch,3*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(1.42*inch, 3.02*inch, amt_hauz)
        else:
            c.setFillColor(white)
            c.rect(0.3*inch,3*inch,0.12*inch,0.12*inch,fill=1)
        if hauz == 'RENTED':
            c.setFillColor(black)
            c.rect(0.3*inch,2.8*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(1.42*inch, 2.82*inch, amt_hauz)
        else:
            c.setFillColor(white)
            c.rect(0.3*inch,2.8*inch,0.12*inch,0.12*inch,fill=1)
        
        if hauz == 'GOVERNMENT':
            c.setFillColor(black)
            c.rect(0.3*inch,2.6*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(1.42*inch, 2.62*inch, amt_hauz)
        else:
            c.setFillColor(white)
            c.rect(0.3*inch,2.6*inch,0.12*inch,0.12*inch,fill=1)
        if hauz == 'PRIVATE':
            c.setFillColor(black)
            c.rect(0.3*inch,2.4*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(1.42*inch, 2.42*inch, amt_hauz)
        else:
            c.setFillColor(white)
            c.rect(0.3*inch,2.4*inch,0.12*inch,0.12*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 10, leading=None)
        c.drawString(0.3*inch, 3.23*inch, "Housing")
        c.drawString(1.4*inch, 3.02*inch, "________________")
        c.drawString(0.5*inch, 3.02*inch, "Owned")
        c.drawString(1.4*inch, 2.82*inch, "________________")
        c.drawString(0.5*inch, 2.82*inch, "Rent")
        c.drawString(1.4*inch, 2.62*inch, "________________")
        c.drawString(0.5*inch, 2.62*inch, "Government")
        c.drawString(1.4*inch, 2.42*inch, "________________")
        c.drawString(0.5*inch, 2.42*inch, "Private")

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(2.1875*inch,2.35*inch,1.9375*inch,1*inch,fill=1)

        c.setLineWidth(1)
        if fls[0] == 'ELECTRICITY':
            c.setFillColor(black)
            c.rect(2.25*inch,3*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(3.02*inch, 3.02*inch, amt_fls[0])
        else:
            c.setFillColor(white)
            c.rect(2.25*inch,3*inch,0.12*inch,0.12*inch,fill=1)
        
        if fls[1] == 'KEROSENE':
            c.setFillColor(black)
            c.rect(2.25*inch,2.8*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(3.02*inch, 2.82*inch, amt_fls[1])
        else:
            c.setFillColor(white)
            c.rect(2.25*inch,2.8*inch,0.12*inch,0.12*inch,fill=1)

        if fls[2] == 'CANDLE':
            c.setFillColor(black)
            c.rect(2.25*inch,2.6*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(3.02*inch, 2.62*inch, amt_fls[2])
        else:
            c.setFillColor(white)
            c.rect(2.25*inch,2.6*inch,0.12*inch,0.12*inch,fill=1)

        if fls[3] == 'OTHERS':
            c.setFillColor(black)
            c.rect(2.25*inch,2.4*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(3.02*inch, 2.42*inch, amt_fls[3])
        else:
            c.setFillColor(white)
            c.rect(2.25*inch,2.4*inch,0.12*inch,0.12*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 10, leading=None)
        c.drawString(2.2*inch, 3.23*inch, "LIGHT SOURCE")
        c.drawString(3*inch, 3.02*inch, "________________")
        c.drawString(2.4*inch, 3.02*inch, "Electricity")
        c.drawString(3*inch, 2.82*inch, "________________")
        c.drawString(2.4*inch, 2.82*inch, "Kerosene")
        c.drawString(3*inch, 2.62*inch, "________________")
        c.drawString(2.4*inch, 2.62*inch, "Candle")
        c.drawString(3*inch, 2.42*inch, "________________")
        c.drawString(2.4*inch, 2.42*inch, "Others")


        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(4.125*inch,2.35*inch,1.9375*inch,1*inch,fill=1)
    
        
        
        

        c.setLineWidth(1)
        if fws[0] == 'PUBLIC':
            c.setFillColor(black)
            c.rect(4.2*inch,3*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(5.22*inch, 3.02*inch, amt_fws[0])
        else:
            c.setFillColor(white)
            c.rect(4.2*inch,3*inch,0.12*inch,0.12*inch,fill=1)

        if fws[1] == 'NATURAL':
            c.setFillColor(black)
            c.rect(4.2*inch,2.4*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(5.22*inch, 2.42*inch, amt_fws[1])
        else:
            c.setFillColor(white)
            c.rect(4.2*inch,2.4*inch,0.12*inch,0.12*inch,fill=1)

        if fws[2] == 'WATERDISTRICT':
            c.setFillColor(black)
            c.rect(4.2*inch,2.6*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(5.22*inch, 2.62*inch, amt_fws[2])
        else:
            c.setFillColor(white)
            c.rect(4.2*inch,2.6*inch,0.12*inch,0.12*inch,fill=1)
        if fws[3] == 'MINERAL':
            c.setFillColor(black)
            c.rect(4.2*inch,2.8*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(5.22*inch, 2.82*inch, amt_fws[3])
        else:
            c.setFillColor(white)
            c.rect(4.2*inch,2.8*inch,0.12*inch,0.12*inch,fill=1)


        c.setFillColor("black")
        c.setFont("Times-Roman", 10, leading=None)
        c.drawString(4.16*inch, 3.23*inch, "WATER SOURCE")
        c.drawString(5.2*inch, 3.02*inch, "________________")
        c.drawString(4.35*inch, 3.02*inch, "Public")
        c.drawString(5.2*inch, 2.82*inch, "________________")
        c.drawString(4.35*inch, 2.82*inch, "Private")
        c.drawString(5.2*inch, 2.62*inch, "________________")
        c.drawString(4.35*inch, 2.62*inch, "Water District")
        c.drawString(5.2*inch, 2.42*inch, "________________")
        c.drawString(4.35*inch, 2.42*inch, "Artesan Well")

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(6.0625*inch,2.35*inch,1.9375*inch,1*inch,fill=1)
        
        
        
        if fuel_src[0]=='LPG':
            c.setFillColor(black)
            c.rect(6.12*inch,3*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(7.12*inch, 3.03*inch, amt_fuel_src[0])
        else:
            c.setFillColor(white)
            c.rect(6.12*inch,3*inch,0.12*inch,0.12*inch,fill=1)
        if fuel_src[1]=='ELECTRIC':
            c.setFillColor(black)
            c.rect(6.12*inch,2.4*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(7.12*inch, 2.43*inch, amt_fuel_src[1])
        else:
            c.setFillColor(white)
            c.rect(6.12*inch,2.4*inch,0.12*inch,0.12*inch,fill=1)
        if fuel_src[2]=='CHARCOAL':
            c.setFillColor(black)
            c.rect(6.12*inch,2.6*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(7.12*inch, 2.63*inch, amt_fuel_src[2])
        else:
            c.setFillColor(white)
            c.rect(6.12*inch,2.6*inch,0.12*inch,0.12*inch,fill=1)
        if fuel_src[3]=='FIREWOOD':
            c.setFillColor(black)
            c.rect(6.12*inch,2.8*inch,0.12*inch,0.12*inch,fill=1)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(7.12*inch, 2.83*inch, amt_fuel_src[3])
        else:
            c.setFillColor(white)
            c.rect(6.12*inch,2.8*inch,0.12*inch,0.12*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 10, leading=None)
        c.drawString(6.09*inch, 3.23*inch, "FUEL SOURCE")
        c.drawString(7.1*inch, 3.02*inch, "_____________")
        c.drawString(6.28*inch, 3.02*inch, "LPG")
        c.drawString(7.1*inch, 2.82*inch, "_____________")
        c.drawString(6.28*inch, 2.82*inch, "FIREWOOD")
        c.drawString(7.1*inch, 2.62*inch, "_____________")
        c.drawString(6.28*inch, 2.62*inch, "CHARCOAL")
        c.drawString(7.1*inch, 2.42*inch, "_____________")
        c.drawString(6.28*inch, 2.42*inch, "OTHERS")

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(0.25*inch,2.05*inch,1.9375*inch,0.3*inch,fill=1)
        c.rect(2.1875*inch,2.05*inch,1.9375*inch,0.3*inch,fill=1)
        c.rect(4.125*inch,2.05*inch,1.9375*inch,0.3*inch,fill=1)
        c.rect(6.0625*inch,2.05*inch,1.9375*inch,0.3*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(1*inch, 2.24*inch, "FOOD")
        c.drawString(2.8*inch, 2.24*inch, "EDUCATION")
        c.drawString(4.8*inch, 2.24*inch, "CLOTHING")
        c.drawString(6.5*inch, 2.24*inch, "TRANSPORTATION")

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(0.25*inch,1.9*inch,1.5*inch,0.15*inch,fill=1)
        c.rect(1.75*inch,1.9*inch,1.5*inch,0.15*inch,fill=1)
        c.rect(3.25*inch,1.9*inch,1.5*inch,0.15*inch,fill=1)
        c.rect(4.75*inch,1.9*inch,1.5*inch,0.15*inch,fill=1)
        c.rect(6.25*inch,1.9*inch,1.75*inch,0.15*inch,fill=1)

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.7*inch, 1.92*inch, "HOUSEHELP")
        c.drawString(1.82*inch, 1.92*inch, "MEDICAL EXPENDITURE")
        c.drawString(3.4*inch, 1.92*inch, "INSURANCE PREMIUM")
        c.drawString(5.3*inch, 1.92*inch, "OTHERS")
        c.drawString(6.25*inch, 1.92*inch, "TOTAL MONTHLY EXPENDITURE")

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(0.25*inch,1.7*inch,1.5*inch,0.2*inch,fill=1)
        c.rect(1.75*inch,1.7*inch,1.5*inch,0.2*inch,fill=1)
        c.rect(3.25*inch,1.7*inch,1.5*inch,0.2*inch,fill=1)
        c.rect(4.75*inch,1.7*inch,1.5*inch,0.2*inch,fill=1)
        c.rect(6.25*inch,1.7*inch,1.75*inch,0.2*inch,fill=1)

        c.setFillColor(black)
        c.setFont("Times-Bold", 8, leading=None)
        tot_expense_cloth = float(tot_expense) + float(clothing_amt)
        total_exp = '{:,.2f}'.format(float(tot_expense_cloth))
        c.drawString(6.4*inch, 1.76*inch, total_exp)
        c.setLineWidth(1)
        if oe[0] == 'HOUSE':
            c.setFillColor("black")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(0.4*inch, 1.76*inch, amt_oe[0])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(0.4*inch, 1.76*inch,"0")
        
        if oe[3] == 'EDU':
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(2.3375*inch, 2.1*inch, amt_oe[3])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(2.3375*inch, 2.1*inch, "0.00")
        if oe[6] == 'FOOD':
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(0.4*inch, 2.1*inch, amt_oe[6])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(0.4*inch, 2.1*inch, "0.00")

        if clothing_amt is not None:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(4.275*inch, 2.1*inch, clothing_amt)
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(4.275*inch, 2.1*inch, "0.00")

        if oe[1] == 'ME':
            c.setFillColor("black")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.79*inch, 1.76*inch, amt_oe[1])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(1.79*inch, 1.76*inch, "0.00")


        if oe[2] == 'IP':
            c.setFillColor("black")
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(3.29*inch, 1.76*inch, amt_oe[2])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(3.29*inch, 1.76*inch, "0.00")
        if oe[5] == 'TRANSPO':
            c.setFillColor(black)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(6.2125*inch, 2.1*inch, amt_oe[5])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 7, leading=None)
            c.drawString(6.2125*inch, 2.1*inch, amt_oe[5])

        if oe[8] == 'OTHER':
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(4.79*inch, 1.76*inch, amt_oe[8])
        else:
            c.setFillColor(black)
            c.setFont("Times-Bold", 8, leading=None)
            c.drawString(4.79*inch, 1.76*inch, "0.00")

        c.setFillColor(skyblue)
        c.rect(0.25*inch,1.55*inch,7.75*inch,0.15*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.28*inch, 1.58*inch, "II. MEDICAL HISTORY")

        c.setFillColor(white)
        c.rect(0.25*inch,1.15*inch,3.875*inch,0.4*inch,fill=1)
        c.rect(4.125*inch,1.15*inch,3.875*inch,0.4*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.28*inch, 1.45*inch, "ADMITTING DIAGNOSIS")
        c.drawString(4.15*inch, 1.45*inch, "FINAL DIAGNOSIS")

        c.setFillColor(white)
        c.rect(0.25*inch,0.85*inch,3.875*inch,0.3*inch,fill=1)
        c.rect(4.125*inch,0.85*inch,3.875*inch,0.3*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.28*inch, 1.05*inch, "DURATION OF PROBLEM/SYMPTOMS")
        c.drawString(4.15*inch, 1.05*inch, "PREVIOUS TREATMENT/DURATION")

        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        p = Paragraph(duration_of_prob, style=custom_font_size)
        p.wrapOn(c, 270,20)  
        p.drawOn(c,0.3*inch,0.88*inch) 
        p = Paragraph(prev_treatment, style=custom_font_size)
        p.wrapOn(c, 270,20)  
        p.drawOn(c,4.2*inch,0.88*inch) 

        c.setFillColor(white)
        c.rect(0.25*inch,0.55*inch,3.875*inch,0.3*inch,fill=1)
        c.rect(4.125*inch,0.55*inch,3.875*inch,0.3*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.28*inch, 0.75*inch, "PRESENT TREATMENT PLAN:")
        c.drawString(4.15*inch, 0.75*inch, "HEALTH ACCESSIBILITY PROBLEM")

        c.setFillColor(black)
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 0.57*inch,"CONFINEMENT")

        p = Paragraph(health_accessibility_prob, style=custom_font_size)
        p.wrapOn(c, 270,20)  
        p.drawOn(c,4.2*inch,0.57*inch) 

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
            p.drawOn(c,0.3*inch,1.18*inch) 

            p = Paragraph(f_prob_desc[0], style=custom_font_size)
            p.wrapOn(c, 270,20)  
            p.drawOn(c,4.2*inch,1.18*inch) 
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

        c.setLineWidth(1)# horizontalline bottom
        c.line(0.25*inch,1.7*inch,8*inch,1.7*inch)

        c.setLineWidth(1)# verticalline left
        c.line(0.25*inch,1.7*inch,0.25*inch,10.45*inch)

        c.setLineWidth(1)# verticalline right
        c.line(8*inch,1.7*inch,8*inch,10.45*inch)

        c.setFillColor(skyblue)
        c.rect(0.25*inch,10.3*inch,7.75*inch,0.15*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.28*inch, 10.32*inch, "II. ASSESSMENT OF SOCIAL FUNCTIONING")

        c.setFillColor(white)
        c.rect(0.25*inch,7.3*inch,7.75*inch,3*inch,fill=1)

        
        
        c.setFillColor(white)#1 family roles
        c.rect(0.25*inch,8.25*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 8.29*inch, "PARENT")

        c.setFillColor(white)
        c.rect(0.25*inch,8.05*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 8.09*inch, "SPOUSE")

        c.setFillColor(white)
        c.rect(0.25*inch,7.85*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 7.89*inch, "CHILD")
        c.setFillColor(white)
        c.rect(0.25*inch,7.65*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 7.69*inch, "SIBLING")

        c.setFillColor(white)
        c.rect(0.25*inch,7.45*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 7.49*inch, "OTHER FAMILY MEMBER")

        c.setFillColor(white)
        c.rect(0.25*inch,7.25*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 7.32*inch, "SIGNIFICANT OTHERS")

        c.setFillColor("black")
        c.setFont("Times-Roman", 7.7, leading=None)
        c.drawString(0.4*inch, 10.2*inch, "1.   FAMILIAL ROLES")
        c.drawString(1.82*inch, 10.2*inch, "TYPE OF SOCIAL INTERACTION")
        c.drawString(1.82*inch, 10.05*inch, "PROBLEM")
        c.drawString(1.82*inch, 9.9*inch, "1. POWER")
        c.drawString(1.82*inch, 9.75*inch, "2. AMBIVALENCE")
        c.drawString(1.82*inch, 9.55*inch, "3. RESPONSIBILITY")
        c.drawString(1.82*inch, 9.35*inch, "4. DEPENDENCY")
        c.drawString(1.82*inch, 9.15*inch, "5. LOSS")
        c.drawString(1.82*inch, 9*inch, "6. ISOLATION")
        c.drawString(1.82*inch, 8.8*inch, "7. VICTIMIZATION")
        c.drawString(1.82*inch, 8.65*inch, "8. MIXED")
        c.drawString(1.82*inch, 8.5*inch, "9. OTHERS")

        c.drawString(3.62*inch, 10.2*inch, "SECERITY INDEX")
        c.drawString(3.64*inch, 10.05*inch, "1. NO PROBLEM")
        c.drawString(3.64*inch, 9.9*inch, "2. LOW")
        c.drawString(3.64*inch, 9.75*inch, "3. MODERATE")
        c.drawString(3.64*inch, 9.55*inch, "4. HIGH")
        c.drawString(3.64*inch, 9.35*inch, "5. VERY HIGH")
        c.drawString(3.64*inch, 9.15*inch, "6. CATASTROPHIC")
        
        c.drawString(5.22*inch, 10.2*inch, "DURATION INDEX")
        c.drawString(5.24*inch, 10.05*inch, "1. More than five years")
        c.drawString(5.24*inch, 9.9*inch, "2. One to five years")
        c.drawString(5.24*inch, 9.75*inch, "3. Six mos to one Year")
        c.drawString(5.24*inch, 9.55*inch, "4. One to six mos")
        c.drawString(5.24*inch, 9.35*inch, "5. Two weeks to one month")
        c.drawString(5.24*inch, 9.15*inch, "6. Less than two weeks")

        c.drawString(6.62*inch, 10.2*inch, "COPING INDEX")
        c.drawString(6.64*inch, 10.05*inch, "1. Outstanding")
        c.drawString(6.64*inch, 9.9*inch, "2. Above average")
        c.drawString(6.64*inch, 9.75*inch, "3. Adequate")
        c.drawString(6.64*inch, 9.55*inch, "4. Somewhat Inadequate")
        c.drawString(6.64*inch, 9.35*inch, "5. Inadequate")
        c.drawString(6.64*inch, 9.15*inch, "6. No coping skills")
        c.setLineWidth(1)# verticalline left 1st
        c.line(1.8*inch,7.25*inch,1.8*inch,10.3*inch)
        c.line(3.6*inch,7.25*inch,3.6*inch,10.3*inch)
        c.line(5.2*inch,7.25*inch,5.2*inch,10.3*inch)
        c.line(6.6*inch,7.25*inch,6.6*inch,10.3*inch)

        c.setLineWidth(1)# verticalline type of social interaction
        c.line(2*inch,7.25*inch,2*inch,8.45*inch)
        c.line(2.2*inch,7.25*inch,2.2*inch,8.45*inch)
        c.line(2.4*inch,7.25*inch,2.4*inch,8.45*inch)
        c.line(2.6*inch,7.25*inch,2.6*inch,8.45*inch)
        c.line(2.8*inch,7.25*inch,2.8*inch,8.45*inch)
        c.line(3*inch,7.25*inch,3*inch,8.45*inch)
        c.line(3.2*inch,7.25*inch,3.2*inch,8.45*inch)
        c.line(3.4*inch,7.25*inch,3.4*inch,8.45*inch)

        c.setLineWidth(1)# severity index
        c.line(3.86*inch,7.25*inch,3.86*inch,8.45*inch)
        c.line(4.11*inch,7.25*inch,4.11*inch,8.45*inch)
        c.line(4.36*inch,7.25*inch,4.36*inch,8.45*inch)
        c.line(4.61*inch,7.25*inch,4.61*inch,8.45*inch)
        c.line(4.87*inch,7.25*inch,4.86*inch,8.45*inch)

        c.setLineWidth(1)# Duration index
        c.line(5.44*inch,7.25*inch,5.44*inch,8.45*inch)
        c.line(5.68*inch,7.25*inch,5.68*inch,8.45*inch)
        c.line(5.92*inch,7.25*inch,5.92*inch,8.45*inch)
        c.line(6.16*inch,7.25*inch,6.16*inch,8.45*inch)
        c.line(6.4*inch,7.25*inch,6.4*inch,8.45*inch)

        c.setLineWidth(1)# Coping index
        c.line(6.85*inch,7.25*inch,6.85*inch,8.45*inch)
        c.line(7.1*inch,7.25*inch,7.1*inch,8.45*inch)
        c.line(7.3*inch,7.25*inch,7.3*inch,8.45*inch)
        c.line(7.5*inch,7.25*inch,7.5*inch,8.45*inch)
        c.line(7.75*inch,7.25*inch,7.75*inch,8.45*inch)
        

        c.setFillColor(white)
        c.rect(0.25*inch,7.13*inch,7.75*inch,0.15*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 7.17*inch, "2.OTHER INTERPERSONAL ROLES")

        c.setFillColor(white)
        c.rect(0.25*inch,6.15*inch,7.75*inch,1*inch,fill=1)

        c.setFillColor(white)#2 other interpersonal roles
        c.rect(0.25*inch,6.95*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 6.99*inch, "Lever")
        c.setFillColor(white)
        c.rect(0.25*inch,6.75*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 6.79*inch, "Friend")
        c.setFillColor(white)
        c.rect(0.25*inch,6.55*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 6.59*inch, "Neighbor")
        c.setFillColor(white)
        c.rect(0.25*inch,6.35*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 6.39*inch, "Member")
        c.setFillColor(white)
        c.rect(0.25*inch,6.15*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 6.23*inch, "Others(Specify)")

        c.setLineWidth(1)# verticalline left 2nd
        c.setFillColor(white)
        c.line(1.8*inch,6.15*inch,1.8*inch,7.15*inch)
        c.line(3.6*inch,6.15*inch,3.6*inch,7.15*inch)
        c.line(5.2*inch,6.15*inch,5.2*inch,7.15*inch)
        c.line(6.6*inch,6.15*inch,6.6*inch,7.15*inch)

        c.setLineWidth(1)# verticalline type of social interaction
        c.setFillColor(white)
        c.line(2*inch,6.15*inch,2*inch,7.15*inch)
        c.line(2.2*inch,6.15*inch,2.2*inch,7.15*inch)
        c.line(2.4*inch,6.15*inch,2.4*inch,7.15*inch)
        c.line(2.6*inch,6.15*inch,2.6*inch,7.15*inch)
        c.line(2.8*inch,6.15*inch,2.8*inch,7.15*inch)
        c.line(3*inch,6.15*inch,3*inch,7.15*inch)
        c.line(3.2*inch,6.15*inch,3.2*inch,7.15*inch)
        c.line(3.4*inch,6.15*inch,3.4*inch,7.15*inch)

        c.setLineWidth(1)# severity index
        c.setFillColor(white)
        c.line(3.86*inch,6.15*inch,3.86*inch,7.15*inch)
        c.line(4.11*inch,6.15*inch,4.11*inch,7.15*inch)
        c.line(4.36*inch,6.15*inch,4.36*inch,7.15*inch)
        c.line(4.61*inch,6.15*inch,4.61*inch,7.15*inch)
        c.line(4.87*inch,6.15*inch,4.86*inch,7.15*inch)

        c.setLineWidth(1)# Duration index
        c.setFillColor(white)
        c.line(5.44*inch,6.15*inch,5.44*inch,7.15*inch)
        c.line(5.68*inch,6.15*inch,5.68*inch,7.15*inch)
        c.line(5.92*inch,6.15*inch,5.92*inch,7.15*inch)
        c.line(6.16*inch,6.15*inch,6.16*inch,7.15*inch)
        c.line(6.4*inch,6.15*inch,6.4*inch,7.15*inch)

        c.setLineWidth(1)# Coping index
        c.setFillColor(white)
        c.line(6.85*inch,6.15*inch,6.85*inch,7.15*inch)
        c.line(7.1*inch,6.15*inch,7.1*inch,7.15*inch)
        c.line(7.3*inch,6.15*inch,7.3*inch,7.15*inch)
        c.line(7.5*inch,6.15*inch,7.5*inch,7.15*inch)
        c.line(7.75*inch,6.15*inch,7.75*inch,7.15*inch)
        
        # c.setFillColor(white)
        # c.rect(0.25*inch,5*inch,7.75*inch,1*inch,fill=1)

        c.setFillColor(white)#3 occupotianal roles roles
        c.rect(0.25*inch,5.8*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 5.86*inch, "Woker-Paid Economy")
        c.setFillColor(white)
        c.rect(0.25*inch,5.6*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 5.66*inch, "Worker-Home")
        c.setFillColor(white)
        c.rect(0.25*inch,5.4*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 5.46*inch, "Worker-Volunteer")
        c.setFillColor(white)
        c.rect(0.25*inch,5.2*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 5.26*inch, "Student")
        c.setFillColor(white)
        c.rect(0.25*inch,5*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 5.06*inch, "Others(Specify)")

        c.setFillColor(white)
        c.rect(0.25*inch,6*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.4*inch, 6.05*inch, "3.OCCUPATIONAL ROLES")

        c.setLineWidth(1)# verticalline left 3rd
        c.line(1.8*inch,5*inch,1.8*inch,6*inch)
        c.line(3.6*inch,5*inch,3.6*inch,6*inch)
        c.line(5.2*inch,5*inch,5.2*inch,6*inch)
        c.line(6.6*inch,5*inch,6.6*inch,6*inch)

        c.setLineWidth(1)# verticalline type of social interaction
        c.line(2*inch,5*inch,2*inch,6*inch)
        c.line(2.2*inch,5*inch,2.2*inch,6*inch)
        c.line(2.4*inch,5*inch,2.4*inch,6*inch)
        c.line(2.6*inch,5*inch,2.6*inch,6*inch)
        c.line(2.8*inch,5*inch,2.8*inch,6*inch)
        c.line(3*inch,5*inch,3*inch,6*inch)
        c.line(3.2*inch,5*inch,3.2*inch,6*inch)
        c.line(3.4*inch,5*inch,3.4*inch,6*inch)

        c.setLineWidth(1)# severity index
        c.line(3.86*inch,5*inch,3.86*inch,6*inch)
        c.line(4.11*inch,5*inch,4.11*inch,6*inch)
        c.line(4.36*inch,5*inch,4.36*inch,6*inch)
        c.line(4.61*inch,5*inch,4.61*inch,6*inch)
        c.line(4.87*inch,5*inch,4.86*inch,6*inch)

        c.setLineWidth(1)# Duration index
        c.line(5.44*inch,5*inch,5.44*inch,6*inch)
        c.line(5.68*inch,5*inch,5.68*inch,6*inch)
        c.line(5.92*inch,5*inch,5.92*inch,6*inch)
        c.line(6.16*inch,5*inch,6.16*inch,6*inch)
        c.line(6.4*inch,5*inch,6.4*inch,6*inch)

        c.setLineWidth(1)# Coping index
        c.line(6.85*inch,5*inch,6.85*inch,6*inch)
        c.line(7.1*inch,5*inch,7.1*inch,6*inch)
        c.line(7.3*inch,5*inch,7.3*inch,6*inch)
        c.line(7.5*inch,5*inch,7.5*inch,6*inch)
        c.line(7.75*inch,5*inch,7.75*inch,6*inch)

        c.setFillColor(white)
        c.rect(0.25*inch,4.85*inch,7.75*inch,0.15*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 4.87*inch, "4. SPECIAL LIFE SITUATION ROLES")


        c.setFillColor(white)
        c.rect(0.25*inch,3.35*inch,7.75*inch,1.5*inch,fill=1)

        c.setFillColor(white)#4 special life situation roles
        c.rect(0.25*inch,4.6625*inch,7.75*inch,0.1875*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 4.71*inch, "Consumner")
        c.setFillColor(white)
        c.rect(0.25*inch,4.475*inch,7.75*inch,0.1875*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 4.52*inch, "Inpatient/Client")

        c.setFillColor(white)
        c.rect(0.25*inch,4.2875*inch,7.75*inch,0.1875*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 4.35*inch, "Outpatient/Client")

        c.setFillColor(white)
        c.rect(0.25*inch,4.1*inch,7.75*inch,0.1875*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 4.16*inch, "Prisoner")

        c.setFillColor(white)
        c.rect(0.25*inch,3.9125*inch,7.75*inch,0.1875*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 3.97*inch, "Immigrant-legal")

        c.setFillColor(white)
        c.rect(0.25*inch,3.725*inch,7.75*inch,0.1875*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 3.78*inch, "Immigrant-illegal")

        c.setFillColor(white)
        c.rect(0.25*inch,3.5375*inch,7.75*inch,0.1875*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 3.6*inch, "Immigrant-refuge")

        c.setFillColor(white)
        c.rect(0.25*inch,3.35*inch,7.75*inch,0.1875*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.4*inch, 3.4*inch, "Others(Specify)")

        c.setLineWidth(1)# verticalline left 3rd
        c.line(1.8*inch,3.35*inch,1.8*inch,4.85*inch)
        c.line(3.6*inch,3.35*inch,3.6*inch,4.85*inch)
        c.line(5.2*inch,3.35*inch,5.2*inch,4.85*inch)
        c.line(6.6*inch,3.35*inch,6.6*inch,4.85*inch)

        c.setLineWidth(1)# verticalline type of social interaction
        c.line(2*inch,3.35*inch,2*inch,4.85*inch)
        c.line(2.2*inch,3.35*inch,2.2*inch,4.85*inch)
        c.line(2.4*inch,3.35*inch,2.4*inch,4.85*inch)
        c.line(2.6*inch,3.35*inch,2.6*inch,4.85*inch)
        c.line(2.8*inch,3.35*inch,2.8*inch,4.85*inch)
        c.line(3*inch,3.35*inch,3*inch,4.85*inch)
        c.line(3.2*inch,3.35*inch,3.2*inch,4.85*inch)
        c.line(3.4*inch,3.35*inch,3.4*inch,4.85*inch)

        c.setLineWidth(1)# severity index
        c.line(3.86*inch,3.35*inch,3.86*inch,4.85*inch)
        c.line(4.11*inch,3.35*inch,4.11*inch,4.85*inch)
        c.line(4.36*inch,3.35*inch,4.36*inch,4.85*inch)
        c.line(4.61*inch,3.35*inch,4.61*inch,4.85*inch)
        c.line(4.87*inch,3.35*inch,4.86*inch,4.85*inch)

        c.setLineWidth(1)# Duration index
        c.line(5.44*inch,3.35*inch,5.44*inch,4.85*inch)
        c.line(5.68*inch,3.35*inch,5.68*inch,4.85*inch)
        c.line(5.92*inch,3.35*inch,5.92*inch,4.85*inch)
        c.line(6.16*inch,3.35*inch,6.16*inch,4.85*inch)
        c.line(6.4*inch,3.35*inch,6.4*inch,4.85*inch)

        c.setLineWidth(1)# Coping index
        c.line(6.85*inch,3.35*inch,6.85*inch,4.85*inch)
        c.line(7.1*inch,3.35*inch,7.1*inch,4.85*inch)
        c.line(7.3*inch,3.35*inch,7.3*inch,4.85*inch)
        c.line(7.5*inch,3.35*inch,7.5*inch,4.85*inch)
        c.line(7.75*inch,3.35*inch,7.75*inch,4.85*inch)
    
        


        c.setFillColor("black")
        c.setFont("Times-Bold", 8, leading=None)
        c.drawString(0.3*inch, 3.2*inch, "NO SOCIAL INTERACTION PROBLEMS")

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
        c.drawString(4.2*inch, 3.66*inch, "RECCOMENDED INTERVENTIONS")

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
        c.setFillColor(white)
        c.rect(0.25*inch,8.05*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 8.1*inch, "2. SHELTER")
        c.setFillColor(white)
        c.rect(0.25*inch,7.25*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 7.3*inch, "3. EMPLOYMENT")
        c.setFillColor(white)
        c.rect(0.25*inch,6.25*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 5.5*inch, "4. ECONOMIC RESOURCES")
        c.setFillColor(white)
        c.rect(0.25*inch,5.45*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 5.5*inch, "5. TRANSPORTATION")
        c.setFillColor(white)
        c.rect(0.25*inch,4.65*inch,7.75*inch,0.2*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Roman", 8, leading=None)
        c.drawString(0.3*inch, 4.7*inch, "B.  AFFECTIONAL SUPPORT SYSTEM")

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
        fxip = cup + 4.95
        c.drawString(fxip*inch, 0.9*inch, request.session['position'] )

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
