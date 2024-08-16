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

def scsr_pdf(request,uis):
    malasakit = 'uis/static/malasakit.png'
    brglogo = 'uis/static/logo.png'
    doh = 'uis/static/doh.png'
    dswd = 'uis/static/dswd.png'
    pcso = 'uis/static/pcso.png'
    philhealth = 'uis/static/philhealth.png'

    get_details = UIS.objects.filter(uis = uis)
    for i in get_details:
        hospno = i.hospno
        philnum = i.phil_no
    informant_details = Informant.objects.filter(uis = uis)
    for a in informant_details:
        doi_init = a.date_of_intake
        date_conv = datetime.strptime(doi_init, '%Y-%m-%d')
        doi = date_conv.strftime('%B %d, %Y')
        informant_time_of_interview = a.time_of_interview
        informant_fullname = a.fullname
        informant_relation_to_patient = a.relation_to_patient
        informant_contact_number = a.contact_number
     
     
    
   
    
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    response = HttpResponse(content_type='application/pdf')
    c.setTitle("SOCIAL CASE STUDY REPORT")
    c.setPageSize((8.27*inch, 11.69*inch))
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    custom_font_size_prob_pres = style.clone('CustomStyle')
    custom_font_size_prob_pres.fontSize = 7
    custom_font_size_prob_pres.leading = 7

    c.drawImage(malasakit, 2.6*inch, 11.2*inch, mask='auto', width=30, height=30)
    c.drawImage(brglogo,3.05*inch, 11.2*inch, mask='auto', width=30, height=30)
    c.drawImage(doh,3.53*inch, 11.2*inch, mask='auto', width=30, height=30)
    c.drawImage(dswd,3.93*inch, 11.2*inch, mask='auto', width=30, height=30)
    c.drawImage(pcso,4.38*inch, 11.2*inch, mask='auto', width=30, height=30)
    c.drawImage(philhealth,4.9*inch, 11.2*inch, mask='auto', width=50, height=30)

    
    c.setLineWidth(2)# horizontalline top)
    c.setStrokeColor(skyblue)
    c.line(0.25*inch,11.05*inch,8*inch,11.05*inch)

    c.setFillColor("black")
    c.setFont("Times-Bold", 10, leading=None)
    c.drawString(3*inch, 10.8*inch, "SOCIAL CASE STUDY REPORT")

    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(0.4*inch, 10.6*inch, "HOMIS NUMBER:")
    c.drawString(0.4*inch, 10.45*inch, "PHILHEALTH NUMBER:")
    c.drawString(6.2*inch, 10.6*inch, "Date:")
    c.drawString(6.2*inch, 10.45*inch, "Time:")
    c.drawString(1.5*inch, 10.6*inch, "____________________________")
    c.drawString(1.52*inch, 10.6*inch, hospno)
    c.drawString(1.52*inch, 10.45*inch, philnum)
    c.drawString(1.5*inch, 10.45*inch, "____________________________")
    c.drawString(6.45*inch, 10.6*inch, "____________________________")
    c.drawString(6.47*inch, 10.6*inch, doi)
    c.drawString(6.45*inch, 10.45*inch, "____________________________")
    c.drawString(6.47*inch, 10.45*inch, informant_time_of_interview)
    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
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
        
        
        # ii_pt = b.patient_type
    scsr = SCSR.objects.filter(uis = uis)
    for sc in scsr:
        employer =sc.employer
        skill = sc.special_skill
        doa_init = datetime.strptime(sc.date_admission, '%Y-%m-%d')
        doa = doa_init.strftime('%B %d, %Y')
        ridat = sc.room
        tdd = sc.tdd
        housing_mat_init = sc.housing_material
        conv_housing_mat = housing_mat_init.replace("[","").replace("]","").replace("'","")
        f_hm = conv_housing_mat.replace(" ","")
        housing_mat = f_hm.split(',')
        fuel_src_init = sc.fuel_source
        conv_fuel_src = fuel_src_init.replace("[","").replace("]","").replace("'","")
        f_fsrc = conv_fuel_src.replace(" ","")
        fuel_src = f_fsrc.split(',')
        prob_pres = sc.problem_presented
        p = Paragraph(prob_pres, style=custom_font_size_prob_pres )
        p.wrapOn(c, 550,20)  
        p.drawOn(c,0.3*inch,3.75*inch) 


    c.drawString(0.3*inch, 10.3*inch, "I. IDENTIFYING INFORMATION")
    c.drawString(0.3*inch, 10.3*inch, "_______________________________")
    c.setFont("Times-Roman", 8, leading=None)
    c.drawString(0.3*inch, 10.15*inch, "NAME:")
    c.drawString(1.32*inch, 10.15*inch, ii_cname)
    c.drawString(6.3*inch, 10.15*inch, ii_gender)
    c.drawString(1.3*inch, 10.15*inch, "_______________________________________________________________                                          SEX:_____________________________")
    c.drawString(0.3*inch, 10*inch, "ADDRESS:")
    c.drawString(1.3*inch, 10*inch, "_____________________________________________________________________________________________________________________")
    c.drawString(1.32*inch, 10*inch, ii_perma)
    c.drawString(0.3*inch, 9.85*inch, "CIVIL STATUS:")
    c.drawString(1.3*inch, 9.85*inch, "__________________________________     AGE:______________________         RELIGION: _______________________________________")
    c.drawString(1.32*inch, 9.85*inch, ii_cstat)
    c.drawString(3.65*inch, 9.85*inch, ii_age)
    c.drawString(5.7*inch, 9.85*inch, ii_rel)
    c.drawString(0.3*inch, 9.7*inch, "DATE OF BIRTH:")
    c.drawString(1.3*inch, 9.7*inch, "__________________________________         PLACE OF BIRTH: ______________________________________________________________")
    c.drawString(1.32*inch, 9.7*inch, ii_dob)
    c.drawString(4.45*inch, 9.7*inch, ii_pob)
    c.drawString(0.3*inch, 9.55*inch, "EDUCATIONAL ATTAINMENT:")
    c.drawString(2.2*inch, 9.55*inch, "_____________________________________________________________________________________________________")
    c.drawString(2.22*inch, 9.55*inch, ii_hea)
    c.drawString(0.3*inch, 9.4*inch, "OCCUPATION:")
    c.drawString(1.3*inch, 9.4*inch, "_________________________________________________________   MONTHLY INCOME: _______________________________________")
    c.drawString(1.32*inch, 9.4*inch, ii_occu)
    c.drawString(5.7*inch, 9.4*inch, ii_mi)
    c.drawString(0.3*inch, 9.25*inch, "EMPLOYER:")
    c.drawString(1.3*inch, 9.25*inch, "_____________________________________________________________________________________________________________________")
    c.setFont("Times-Roman", 8, leading=None)
    c.drawString(1.32*inch, 9.25*inch, employer)

    c.drawString(0.3*inch, 9*inch, "SPECIAL SKILLS:")
    
    c.drawString(1.3*inch, 9*inch, "_____________________________________________________________________________________________________________________")
    c.drawString(1.32*inch, 9*inch, skill)
    c.drawString(0.3*inch, 8.85*inch, "DATE OF ADMISSION:")
    c.drawString(2.2*inch, 8.85*inch, "________________________________________________  ROOM IN DATE AND TIME:   _________________________")
    c.drawString(2.22*inch, 8.85*inch, doa)
    c.drawString(6.42*inch, 8.85*inch, ridat)
    c.drawString(0.3*inch, 8.7*inch, "TYPE OF DEFORMITY/DISABILITY:")
    c.drawString(2.2*inch, 8.7*inch, "_____________________________________________________________________________________________________")
    c.drawString(2.22*inch, 8.7*inch, tdd)
    c.drawString(0.3*inch, 8.58*inch, "II. FAMILY COMPOSITION:")

    
    c.setLineWidth(1)
    c.setStrokeColor(black)
    c.setFillColor(white)
    a =0.15
    b = 8.4
    for i in range(11):
        c.rect(0.25*inch,b*inch,1.5*inch,0.15*inch,fill=1)
        c.rect(1.75*inch,b*inch,1.5*inch,0.15*inch,fill=1)
        c.rect(3.25*inch,b*inch,0.3*inch,0.15*inch,fill=1)
        c.rect(3.55*inch,b*inch,0.3*inch,0.15*inch,fill=1)
        c.rect(3.85*inch,b*inch,0.5*inch,0.15*inch,fill=1)
        c.rect(4.35*inch,b*inch,1.5*inch,0.15*inch,fill=1)
        c.rect(5.85*inch,b*inch,1*inch,0.15*inch,fill=1)
        c.rect(6.85*inch,b*inch,1*inch,0.15*inch,fill=1)
        b -= a
    famcom = FamilyComposition.objects.filter(uis = uis)
    pp =0.15
    tt = 8.27
    for cc in famcom:
        c.setFillColor("black")
        c.setFont("Times-Bold", 6.5, leading=None)
        c.drawString(0.27*inch, tt *inch, cc.fullname)
        c.drawString(1.77*inch, tt *inch, cc.relation_to_patient)
        c.drawString(3.34*inch, tt *inch, cc.age)
        # c.drawString(3.56*inch, tt *inch, cc.gender)
        if cc.gender == 'FEMALE':
            c.drawString(3.65*inch, tt *inch, "F")
        elif cc.gender == 'MALE':
            c.drawString(3.65*inch, tt *inch, "M")
        else:
            c.drawString(3.15*inch, tt *inch, "N/A")
        c.drawString(3.86*inch, tt *inch, cc.cstat)
        c.drawString(4.37*inch, tt *inch, cc.hea)
        c.drawString(5.87*inch, tt *inch, cc.occupation)
        famcom_mi = '{:,.2f}'.format(float(cc.mi))
        c.drawString(6.87*inch, tt *inch, famcom_mi)
        tt -=pp
    
    c.setFillColor("black")
    c.setFont("Times-Roman", 7.5, leading=None)
    c.drawString(0.8*inch, 8.42*inch, "NAME")
    c.drawString(2.1*inch, 8.42*inch, "RELATIONSHIP")
    c.drawString(3.28*inch, 8.42*inch, "AGE")
    c.drawString(3.6*inch, 8.42*inch, "SEX")
    c.drawString(3.95*inch, 8.42*inch, "CIVIL")
    c.drawString(4.37*inch, 8.42*inch, "EDUCATIONAL ATTAINMENT")
    c.drawString(5.99*inch, 8.42*inch, "OCCUPATION")
    c.drawString(7.12*inch, 8.42*inch, "INCOME")

    list_of_expenses = ListofExpenses.objects.filter(uis = uis)
    for  oo in list_of_expenses:
        hauz = oo.house
        amt_hauz = oo.amt_house
        lot = oo.lot
        amt_lot = oo.amt_lot
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

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(0.3*inch, 6.7*inch, "HOUSE")
    c.drawString(0.3*inch, 6.7*inch, "_______")
    c.drawString(1.7*inch, 6.7*inch, "AMOUNT")
    c.drawString(1.7*inch, 6.7*inch, "_________")

    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(2.65*inch, 6.7*inch, "HOUSING MATERIAL")
    c.drawString(2.65*inch, 6.7*inch, "____________________")
    c.drawString(3.85*inch, 6.7*inch, "FUEL SOURCE")
    c.drawString(3.85*inch, 6.7*inch, "______________")

    c.setLineWidth(1)
    if housing_mat[0] == 'LIGHT/NATIVE':
        c.setFillColor(black)
        c.rect(2.65*inch,6.55*inch,0.09*inch,0.09*inch,fill=1)
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,6.55*inch,0.09*inch,0.09*inch,fill=1)
    if housing_mat[1] == 'CONCRETE':
        c.setFillColor(black)
        c.rect(2.65*inch,6.4*inch,0.09*inch,0.09*inch,fill=1)
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,6.4*inch,0.09*inch,0.09*inch,fill=1)
    if housing_mat[2] == 'MIXED':
        c.setFillColor(black)
        c.rect(2.65*inch,6.25*inch,0.09*inch,0.09*inch,fill=1)
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,6.25*inch,0.09*inch,0.09*inch,fill=1)
    if fuel_src[0]=='LPG':
        c.setFillColor(black)
        c.rect(3.85*inch,6.55*inch,0.09*inch,0.09*inch,fill=1)
    else:
        c.setFillColor(white)
        c.rect(3.85*inch,6.55*inch,0.09*inch,0.09*inch,fill=1)
    if fuel_src[1]=='ELECTRIC':
        c.setFillColor(black)
        c.rect(3.85*inch,6.4*inch,0.09*inch,0.09*inch,fill=1)
    else:
        c.setFillColor(white)
        c.rect(3.85*inch,6.4*inch,0.09*inch,0.09*inch,fill=1)
    if fuel_src[2]=='CHARCOAL':
        c.setFillColor(black)
        c.rect(3.85*inch,6.25*inch,0.09*inch,0.09*inch,fill=1)
    else:
        c.setFillColor(white)
        c.rect(3.85*inch,6.25*inch,0.09*inch,0.09*inch,fill=1)
    if fuel_src[3]=='FIREWOOD':
        c.setFillColor(black)
        c.rect(3.85*inch,6.1*inch,0.09*inch,0.09*inch,fill=1)
    else:
        c.setFillColor(white)
        c.rect(3.85*inch,6.1*inch,0.09*inch,0.09*inch,fill=1)

    # c.setFillColor(white)
    # c.rect(2.65*inch,4.85*inch,0.09*inch,0.09*inch,fill=1)

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(2.8*inch, 6.55*inch, "LIGHT/NATIVE")
    c.drawString(2.8*inch, 6.4*inch, "CONCRETE")
    c.drawString(2.8*inch, 6.25*inch, "MIXED")

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(4*inch, 6.55*inch, "LPG")
    c.drawString(4*inch, 6.4*inch, "ELECTRIC")
    c.drawString(4*inch, 6.25*inch, "CHARCOAL")
    c.drawString(4*inch, 6.1*inch, "FIREWOOD")
  

    # c.setFont("Times-Bold", 7, leading=None)
    # c.drawString(2.8*inch, 4.85*inch, "OTHERS")
    # c.drawString(3.6*inch, 4.85*inch, "_________________")

    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(2.65*inch, 5.9*inch, "WATER SOURCE")
    c.drawString(2.65*inch, 5.9*inch, "_______________")
    c.drawString(3.85*inch, 5.9*inch, "AMOUNT")
    c.drawString(3.85*inch, 5.9*inch, "_________")

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(2.8*inch, 5.75*inch, "PUBLIC")
    c.drawString(3.6*inch, 5.75*inch, "___________________________")

    c.drawString(2.8*inch, 5.6*inch, "NATURAL")
    c.drawString(3.6*inch, 5.6*inch, "___________________________")

    c.drawString(2.8*inch, 5.45*inch, "WATER DISTRICT")
    c.drawString(3.6*inch, 5.45*inch, "___________________________")

    c.drawString(2.8*inch, 5.3*inch, "MINERAL BUY")
    c.drawString(3.6*inch, 5.3*inch, "___________________________")

    c.setLineWidth(1)
    if fws[0] == 'PUBLIC':
        c.setFillColor(black)
        c.rect(2.65*inch,5.75*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(3.7*inch, 5.75*inch, amt_fws[0])
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,5.75*inch,0.09*inch,0.09*inch,fill=1)

    if fws[1] == 'NATURAL':
        c.setFillColor(black)
        c.rect(2.65*inch,5.6*inch,0.1*inch,0.1*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(3.7*inch, 5.6*inch, amt_fws[1])
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,5.6*inch,0.1*inch,0.1*inch,fill=1)

    if fws[2] == 'WATERDISTRICT':
        c.setFillColor(black)
        c.rect(2.65*inch,5.45*inch,0.1*inch,0.1*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(3.7*inch, 5.45*inch, amt_fws[2])
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,5.45*inch,0.1*inch,0.1*inch,fill=1)
    if fws[3] == 'MINERAL':
        c.setFillColor(black)
        c.rect(2.65*inch,5.3*inch,0.1*inch,0.1*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(3.7*inch, 5.3*inch, amt_fws[3])
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,5.3*inch,0.1*inch,0.1*inch,fill=1)

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(0.47*inch, 6.55*inch, "OWNED")
    c.drawString(1.57*inch, 6.55*inch, "_________________")


    c.drawString(0.47*inch, 6.4*inch, "RENTED")
    c.drawString(1.57*inch, 6.4*inch, "_________________")

    c.drawString(0.47*inch, 6.25*inch, "SHARED")
    c.drawString(1.57*inch, 6.25*inch, "_________________")

    c.drawString(0.47*inch, 6.1*inch, "OTHERS")
    c.drawString(1.57*inch, 6.1*inch, "_________________")
    
    

    c.setLineWidth(1)
    if hauz == 'OWNED': #house
        c.setFillColor(black)
        c.rect(0.3*inch,6.55*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(1.59*inch, 6.55*inch, amt_hauz)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,6.55*inch,0.09*inch,0.09*inch,fill=1)
    if hauz == 'RENTED':
        c.setFillColor(black)
        c.rect(0.3*inch,6.4*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(1.59*inch, 6.4*inch, amt_hauz)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,6.4*inch,0.09*inch,0.09*inch,fill=1)
    
    if hauz == 'SHARED':
        c.setFillColor(black)
        c.rect(0.3*inch,6.25*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(1.59*inch, 6.25*inch, amt_hauz)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,6.25*inch,0.09*inch,0.09*inch,fill=1)
    if hauz == 'OTHERS':
        c.setFillColor(black)
        c.rect(0.3*inch,6.1*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(1.59*inch, 6.1*inch, amt_hauz)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,6.1*inch,0.09*inch,0.09*inch,fill=1)

 

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(0.3*inch, 5.9*inch, "LOT")
    c.drawString(0.3*inch, 5.9*inch, "____")

    c.drawString(1.7*inch, 5.9*inch, "AMOUNT")
    c.drawString(1.7*inch, 5.9*inch, "_________")

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(0.47*inch, 5.75*inch, "OWNED")
    c.drawString(1.57*inch, 5.75*inch, "_________________")

    c.drawString(0.47*inch, 5.6*inch, "SHARED")
    c.drawString(1.57*inch, 5.6*inch, "_________________")

    c.drawString(0.47*inch, 5.45*inch, "GOVERNMENT")
    c.drawString(1.57*inch, 5.45*inch, "_________________")

    c.drawString(0.47*inch, 5.3*inch, "PRIVATE PROPERTY")
    c.drawString(1.57*inch, 5.3*inch, "_________________")

    c.setLineWidth(1)
    if lot == 'OWNED': #lot
        c.setFillColor(black)
        c.rect(0.3*inch,5.75*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(1.59*inch, 5.75*inch, amt_lot)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,5.75*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(1.59*inch, 5.75*inch, "-")

    if lot == 'SHARED':
        c.setFillColor(black)
        c.rect(0.3*inch,5.6*inch,0.1*inch,0.1*inch,fill=1)
        c.drawString(1.59*inch, 5.6*inch, amt_lot)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,5.6*inch,0.1*inch,0.1*inch,fill=1)
        c.drawString(1.59*inch, 5.6*inch, "-")
    if lot == 'GOVERNMENT':
        c.setFillColor(black)
        c.rect(0.3*inch,5.45*inch,0.1*inch,0.1*inch,fill=1)
        c.drawString(1.59*inch, 5.45*inch, amt_lot)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,5.45*inch,0.1*inch,0.1*inch,fill=1)
        c.drawString(1.59*inch, 5.45*inch, "-")
    if lot == 'PRIVATE PROPERTY':
        c.setFillColor(black)
        c.rect(0.3*inch,5.3*inch,0.1*inch,0.1*inch,fill=1)
        c.drawString(1.59*inch, 5.3*inch, amt_lot)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,5.3*inch,0.1*inch,0.1*inch,fill=1)
        c.drawString(1.59*inch, 5.3*inch, "-")


    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(5.45*inch, 6.7*inch, "OTHER EXPENSES")
    c.drawString(5.45*inch, 6.7*inch, "_________________")
    c.drawString(7.2*inch, 6.7*inch, "AMOUNT")
    c.drawString(7.2*inch, 6.7*inch, "_________")


    c.setFillColor(white)
    c.rect(5*inch,5.5*inch,0.09*inch,0.09*inch,fill=1)

    c.setFillColor(white)
    c.rect(5*inch,5.35*inch,0.09*inch,0.09*inch,fill=1)

    c.setLineWidth(1)
    if oe[0] == 'HOUSE':
        c.setFillColor(black)
        c.rect(5*inch,6.55*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 6.55*inch, amt_oe[0])
    else:
        c.setFillColor(white)
        c.rect(5*inch,6.55*inch,0.09*inch,0.09*inch,fill=1)
    
    if oe[3] == 'EDU':
        c.setFillColor(black)
        c.rect(5*inch,6.4*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 6.4*inch, amt_oe[3])
    else:
        c.setFillColor(white)
        c.rect(5*inch,6.4*inch,0.09*inch,0.09*inch,fill=1)
    if oe[6] == 'FOOD':
        c.setFillColor(black)
        c.rect(5*inch,6.25*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 6.25*inch, amt_oe[6])
    else:
        c.setFillColor(white)
        c.rect(5*inch,6.25*inch,0.09*inch,0.09*inch,fill=1)

    if oe[1] == 'ME':
        c.setFillColor(black)
        c.rect(5*inch,6.1*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 6.1*inch, amt_oe[1])
    else:
        c.setFillColor(white)
        c.rect(5*inch,6.1*inch,0.09*inch,0.09*inch,fill=1)

    if oe[4] == 'LOAN':
        c.setFillColor(black)
        c.rect(5*inch,5.95*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 5.95*inch, amt_oe[4])
    else:
        c.setFillColor(white)
        c.rect(5*inch,5.95*inch,0.09*inch,0.09*inch,fill=1)

    if oe[7] == 'SAVINGS':
        c.setFillColor(black)
        c.rect(5*inch,5.8*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 5.8*inch, amt_oe[7])
    else:
        c.setFillColor(white)
        c.rect(5*inch,5.8*inch,0.09*inch,0.09*inch,fill=1)

    if oe[2] == 'IP':
        c.setFillColor(black)
        c.rect(5*inch,5.65*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 5.65*inch, amt_oe[2])
    else:
        c.setFillColor(white)
        c.rect(5*inch,5.65*inch,0.09*inch,0.09*inch,fill=1)
    if oe[5] == 'TRANSPO':
        c.setFillColor(black)
        c.rect(5*inch,5.5*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 5.5*inch, amt_oe[5])
    else:
        c.setFillColor(white)
        c.rect(5*inch,5.5*inch,0.09*inch,0.09*inch,fill=1)

    if oe[8] == 'OTHER':
        c.setFillColor(black)
        c.rect(5*inch,5.35*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 5.35*inch, amt_oe[8])
    else:
        c.setFillColor(white)
        c.rect(5*inch,5.35*inch,0.09*inch,0.09*inch,fill=1)

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(5.2*inch, 6.55*inch, "HOUSEHELP")
    c.drawString(6.7*inch, 6.55*inch, "___________________________")


    c.drawString(5.2*inch, 6.4*inch, "EDUCATION")
    c.drawString(6.7*inch, 6.4*inch, "___________________________")

    c.drawString(5.2*inch, 6.25*inch, "FOOD")
    c.drawString(6.7*inch, 6.25*inch, "___________________________")

    c.drawString(5.2*inch, 6.1*inch, "MEDICAL EXPENDITURES")
    c.drawString(6.7*inch, 6.1*inch, "___________________________")

    c.drawString(5.2*inch, 5.95*inch, "LOAN")
    c.drawString(6.7*inch, 5.95*inch, "___________________________")


    c.drawString(5.2*inch, 5.8*inch, "SAVINGS")
    c.drawString(6.7*inch, 5.8*inch, "___________________________")

    c.drawString(5.2*inch, 5.65*inch, "INSURANCE PREMIUM")
    c.drawString(6.7*inch, 5.65*inch, "___________________________")

    c.drawString(5.2*inch, 5.5*inch, "TRANSPORTATION")
    c.drawString(6.7*inch, 5.5*inch, "___________________________")

    c.drawString(5.2*inch, 5.35*inch, "OTHERS")
    c.drawString(6.7*inch, 5.35*inch, "___________________________")

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(0.8*inch, 5.15*inch, "OTHER SOURCES OF INCOME")
    c.drawString(0.8*inch, 5.15*inch, "____________________________")
    c.drawString(2.85*inch, 5.15*inch, "AMOUNT")
    c.drawString(2.85*inch, 5.15*inch, "_________")
    c.drawString(4*inch, 5.15*inch, "REGULAR")
    c.drawString(4*inch, 5.15*inch, "__________")

    

    ae =0.15
    be = 5
    for i in range(4):
        c.drawString(0.3*inch, be*inch, "___________________________________________")
        c.drawString(2.65*inch, be*inch, "___________________")
        c.drawString(3.63*inch, be*inch, "  _________________________")
        be -= ae
    xe = 0.15
    ye = 5.02
    famcom_osof = Fc_other_source.objects.filter(uis = uis)
    for fo in famcom_osof:
        c.setFont("Times-Bold", 6.5, leading=None)
        c.drawString(0.35*inch, ye*inch, fo.otherSources_of_fi_desc)
        tot_income_osof = '{:,.2f}'.format(float(fo.otherSources_of_fi))
        c.drawString(3.7*inch, ye*inch, tot_income_osof)
        ye -= xe

    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.3*inch, 4.4*inch, "IV. PROBELEM PRESENTED")
    c.drawString(0.3*inch, 4.4*inch, "___________________________")



    c.setLineWidth(1)# horizontalline top)
    c.line(0.25*inch,3.6*inch,8*inch,3.6*inch)
    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.3*inch, 3.4*inch, "V. FINDINGS AND RECOMMENDATIONS")
    c.drawString(0.3*inch, 3.4*inch, "_______________________________________")
    swa_desc = SWA.objects.filter(uis = uis)
    

    for sw in swa_desc:
        desc_swa = sw.swa_desc
        p = Paragraph(desc_swa, style=custom_font_size_prob_pres )
        p.wrapOn(c, 540,20)
        p.drawOn(c,0.3*inch,1.8*inch)
        

    c.setLineWidth(1)# horizontalline top)
    c.line(0.25*inch,1.6*inch,8*inch,1.6*inch)

    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.3*inch, 1.4*inch, "VI. INFORMANT/RELATION TO PATIENT/CONTACT NUMBER")
    c.drawString(0.3*inch, 1.4*inch, "____________________________________________________________")  
    c.drawString(0.35*inch, 1.15 *inch, informant_fullname +" / "+ informant_relation_to_patient +" / "+ informant_contact_number)

    c.setLineWidth(1)# horizontalline top)
    c.line(0.25*inch,1*inch,8*inch,1*inch)

    c.setFillColor("black")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.3*inch, 0.8*inch, "PREPARED BY:")
    c.drawString(0.3*inch, 0.6*inch, "____________________________________________________________")
    # c.drawString(1.3*inch, 0.45*inch, "Social Worker Officer")
    uw = c.stringWidth(request.session['name'])/100
    uiw = 210/100
    cu = (uiw - uw) / 2
    fxi = cu + 0.55
    c.drawString(fxi*inch, 0.62*inch, request.session['name'])

    uw_p = c.stringWidth(request.session['position'])/100
    uiw_p = 210/100
    cu_p = (uiw_p - uw_p) / 2
    fxi_p = cu_p + 0.55
    c.drawString(fxi_p*inch, 0.47*inch, request.session['position'])
    

    c.showPage()
    c.save()
    pdf = buf.getvalue()
    buf.close()
    response.write(pdf)
    return response
