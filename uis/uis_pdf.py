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

def uis_pdf(request,uis):
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
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    response = HttpResponse(content_type='application/pdf')
    c.setTitle("UNIFIED INTAKE SHEET")
    c.setPageSize((8.27*inch, 11.69*inch))
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    custom_font_size = style.clone('CustomStyle')
    custom_font_size_swa = style.clone('CustomStyle')
    custom_font_size.fontSize = 5
    custom_font_size.leading = 5
    custom_font_size_swa.fontSize = 6.5
    custom_font_size_swa.leading = 6.5
    c.drawImage(malasakit, 2.6*inch, 11.2*inch, mask='auto', width=30, height=30)
    c.drawImage(brglogo,3.05*inch, 11.2*inch, mask='auto', width=30, height=30)
    c.drawImage(doh,3.53*inch, 11.2*inch, mask='auto', width=30, height=30)
    c.drawImage(dswd,3.93*inch, 11.2*inch, mask='auto', width=30, height=30)
    c.drawImage(pcso,4.38*inch, 11.2*inch, mask='auto', width=30, height=30)
    c.drawImage(philhealth,4.9*inch, 11.2*inch, mask='auto', width=50, height=30)

    c.setFillColor("black")
    c.setFont("Times-Bold", 10, leading=None)
    c.drawString(3.3*inch, 11.05*inch, "UNIFIED INTAKE SHEET")

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(0.3*inch, 10.85*inch, "Philhealth Identification No")
    c.drawString(1.5*inch, 10.84*inch, "_______________________________________________")
    c.drawString(2.1*inch, 10.86*inch, philnum)

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(6*inch, 10.85*inch, "Hospital No")
    c.drawString(6.5*inch, 10.85*inch, "_______________________________")
    c.drawString(7.1*inch, 10.86*inch, hospno[-6:])

    # square
    c.setFillColor(white)
    c.rect(0.25*inch,0.25*inch,7.8*inch,10.55*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    

    c.setFillColor(skyblue)
    c.rect(0.25*inch,10.15*inch,7.8*inch,0.1*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.3*inch, 10.17*inch, "I. IDENTIFYING INFORMATION (Impormation ng Pagkakakilanlan)")

    c.setFillColor(skyblue)
    c.rect(0.25*inch,8.15*inch,7.8*inch,0.1*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.3*inch, 8.16*inch, "II. FAMILY COMPOSITION")

    c.setFillColor(skyblue)
    c.rect(0.25*inch,5.55*inch,7.8*inch,0.1*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.3*inch, 5.56*inch, "III. LIST OF EXPENSES(Mga Buwanang gastusin)")

    c.setFillColor(skyblue)
    c.rect(0.25*inch,4*inch,7.8*inch,0.1*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.3*inch, 4.01*inch, "IV. PROBLEM PRESENTED(Problemang Idinulog)")

    c.setFillColor(skyblue)
    c.rect(0.25*inch,2.3*inch,7.8*inch,0.1*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.3*inch, 2.31*inch, "V. SOCIAL WORKER ASSESMENT(Pagtatasa ng Social Worker)")

    c.setFillColor(skyblue)
    c.rect(0.25*inch,1.35*inch,7.8*inch,0.1*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.3*inch, 1.36*inch, "VI. RECOMMENDATIONS(Rekomendasyon)")

    get_uis = UIS.objects.filter(uis = uis)
    for gu in get_uis:
        total_income = gu.total_income
        tot_income = '{:,.2f}'.format(float(total_income))
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
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(0.3*inch, 10.65*inch, "Date of Intake/Interview(Petsa ng Panayam)")
    c.drawString(2.2*inch, 10.65*inch, "__________________________________")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(2.3*inch, 10.65*inch, doi)

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(4.7*inch, 10.65*inch, "Time of Interview(Oras ng Panayam)")
    c.drawString(6.27*inch, 10.65*inch, "__________________________________")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(6.27*inch, 10.65*inch, informant_time_of_interview)
    

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(0.3*inch, 10.46*inch, "Name of Informant (Pangalan ng Impormante)")
    c.drawString(2.3*inch, 10.46*inch, "____________________________________________")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(2.3*inch, 10.46*inch, informant_fullname)


    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(4.6*inch, 10.46*inch, "Relation to patient (Relasyon sa Pasyente)")
    c.drawString(6.35*inch, 10.46*inch, "_________________________________")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(6.35*inch, 10.46*inch, informant_relation_to_patient)

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(0.3*inch, 10.3*inch, "Address (Tirahan)")
    c.drawString(1.1*inch, 10.3*inch, "_____________________________________________________________________")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(1.1*inch, 10.3*inch, informant_address)
   

    c.setFillColor("black")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(4.6*inch, 10.3*inch, "Contact Number (Telepono Bilang)")
    c.drawString(6.2*inch, 10.3*inch, "____________________________________")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(6.2*inch, 10.3*inch, informant_contact_number)

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
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.5*inch, 10*inch, "Client's Name")
    c.setFont("Times-Roman", 6, leading=None)
    c.drawString(0.44*inch, 9.9*inch, "(pangalan ng Pasyente)")
    c.drawString(2.5*inch, 9.9*inch, "Last Name(Apelyido), First Name(Pangalan),Middle Name(Gitnang Pangalan) Ext.(Sr.Jr)")
    c.drawString(1.3*inch, 9.98*inch, "               ___________________________________________________________________________________________________________________")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(1.9*inch, 10*inch, ii_cname)

    c.setFont("Times-Roman", 6, leading=None)
    c.drawString(7.4*inch, 9.87*inch, "Sex/Seks")
    c.drawString(7*inch, 9.98*inch, "________________________")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(7.3*inch, 10*inch, ii_gender)

    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.4*inch, 9.75*inch, ii_dob)
    c.drawString(0.25*inch, 9.74*inch, "________________________")
    c.setFont("Times-Roman", 6, leading=None)
    c.drawString(0.27*inch, 9.65*inch, "Date of Birth(Petsa ng kapanganakan)")
    c.setFont("Times-Roman", 6, leading=None)
    c.drawString(2*inch, 9.74*inch, "________________________")
    c.drawString(2.27*inch, 9.65*inch, "Age(Edad)")
    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(2.4*inch, 9.75*inch, ii_age)
    c.setFont("Times-Roman", 6, leading=None)
    c.drawString(5.3*inch, 9.65*inch, "Place of Birth")
    c.drawString(3.5*inch, 9.74*inch, "____________________________________________________________________________________________________________")
    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(3.6*inch, 9.75*inch, ii_pob)


    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.5*inch, 9.4*inch, "Permanent Address")
    c.setFont("Times-Roman", 6, leading=None)
    c.drawString(0.51*inch, 9.33*inch, "(Permanenteng Tirahan)")
    c.drawString(3.6*inch, 9.33*inch, "St. no., Barangay, City/Municipality, District, Province Region")
    c.setFont("Times-Bold", 6, leading=None)
    c.drawString(1.6*inch, 9.4*inch, "__________________________________________________________________________________________________________________________________________________________")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(1.8*inch, 9.41*inch, ii_perma)

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.5*inch, 9.2*inch, "Present Address")
    c.setFont("Times-Roman", 6, leading=None)
    c.drawString(0.51*inch, 9.13*inch, "(Kasalukuyang Tirahan)")
    c.drawString(3.6*inch, 9.05*inch, "St. no., Barangay, City/Municipality, District, Province Region")
    c.setFont("Times-Bold", 6, leading=None)
    c.drawString(1.6*inch, 9.13*inch, "__________________________________________________________________________________________________________________________________________________________")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(1.8*inch, 9.15*inch, ii_pra)

    c.setFont("Times-Roman", 8, leading=None)
    c.drawString(1*inch, 8.9*inch, "Civil Status")

    if ii_cstat == 'SINGLE':
        c.setFillColor(black)#single
        c.rect(1.8*inch,8.9*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(white)#single
        c.rect(1.8*inch,8.9*inch,0.1*inch,0.1*inch,fill=1)

    if ii_cstat == 'MARRIED':
        c.setFillColor(black)#married
        c.rect(2.5*inch,8.9*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(white)#married
        c.rect(2.5*inch,8.9*inch,0.1*inch,0.1*inch,fill=1)

    if ii_cstat == 'WIDOWED':
        c.setFillColor(black)#widow
        c.rect(4*inch,8.9*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(white)#widow
        c.rect(4*inch,8.9*inch,0.1*inch,0.1*inch,fill=1)

    if ii_cstat == 'OTHERS':
        c.setFillColor(black)#others
        c.rect(6*inch,8.9*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(white)#others
        c.rect(6*inch,8.9*inch,0.1*inch,0.1*inch,fill=1)
        c.setFillColor("black")
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.75*inch, 8.9*inch, ii_cstat)

    c.setFillColor("black")
    c.setFont("Times-Roman", 8, leading=None)
    c.drawString(2*inch, 8.9*inch, "Single")
    c.drawString(2.7*inch, 8.9*inch, "Married")
    c.drawString(4.2*inch, 8.9*inch, "Widow/Widower")
    c.drawString(6.2*inch, 8.9*inch, "Others        _______________________")



    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.5*inch, 8.74*inch, "Religion (Relehiyon)")
    c.drawString(1.6*inch, 8.74*inch, "___________________________________")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(1.7*inch, 8.75*inch, ii_rel)

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(4.5*inch, 8.74*inch, "Nationality (Nasyonalidad)")
    c.drawString(5.7*inch, 8.74*inch, "_______________________________________________")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(5.8*inch, 8.75*inch, ii_nat)

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.5*inch, 8.63*inch, "Highest Educational Attainment")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(0.65*inch, 8.55*inch, "(Pinakataas na Edukasyon)")

    if ii_hea == 'POST-GRADUATE':
        c.setFillColor(black)#Post-Graduate
        c.rect(2.5*inch,8.55*inch,0.1*inch,0.1*inch,fill=1)
    else:       
        c.setFillColor(white)#Post-Graduate
        c.rect(2.5*inch,8.55*inch,0.1*inch,0.1*inch,fill=1)

    if ii_hea == 'COLLEGE':
        c.setFillColor(black)#College
        c.rect(4*inch,8.55*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(white)#College
        c.rect(4*inch,8.55*inch,0.1*inch,0.1*inch,fill=1)
    
    if ii_hea == 'HIGH SCHOOL':
        c.setFillColor(black)#high school
        c.rect(5*inch,8.55*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(white)#high school
        c.rect(5*inch,8.55*inch,0.1*inch,0.1*inch,fill=1)

    if ii_hea == 'ELEMENTARY':
        c.setFillColor(black)#elementary   
        c.rect(6*inch,8.55*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(white)#elementary   
        c.rect(6*inch,8.55*inch,0.1*inch,0.1*inch,fill=1)
    
    if ii_hea == 'NONE':
        c.setFillColor(black)#none
        c.rect(7*inch,8.55*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(white)#none
        c.rect(7*inch,8.55*inch,0.1*inch,0.1*inch,fill=1)

    c.setFillColor("black")
    c.setFont("Times-Roman", 8, leading=None)
    c.drawString(2.7*inch, 8.55*inch, "Post-Graduate")
    c.setFont("Times-Roman", 8, leading=None)
    c.drawString(4.2*inch, 8.55*inch, "College")
    c.drawString(5.2*inch, 8.55*inch, "High School")
    c.drawString(6.2*inch, 8.55*inch, "Elementary")
    c.drawString(7.2*inch, 8.55*inch, "None")


    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.5*inch, 8.4*inch, "Occupation(Trabaho)")
    c.drawString(1.6*inch, 8.4*inch, "_________________________________________________________")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(1.7*inch, 8.4*inch, ii_occu)

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(4.7*inch, 8.4*inch, "Monthly Income (Kinikita kada buwan)")
    c.drawString(6.4*inch, 8.4*inch, "_________________________________")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(6.5*inch, 8.4*inch, ii_mi)

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(6.5*inch, 8.28*inch, "Patient Type:")
    c.drawString(7.15*inch, 8.28*inch, "__________________")
   
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(7.17*inch, 8.28*inch, ii_pt)

    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(0.25*inch,8*inch,2.8*inch,0.15*inch,fill=1)
    c.rect(3.05*inch,8*inch,0.3*inch,0.15*inch,fill=1)
    c.rect(3.35*inch,8*inch,0.55*inch,0.15*inch,fill=1)
    c.rect(3.9*inch,8*inch,1*inch,0.15*inch,fill=1)
    c.rect(4.9*inch,8*inch,1*inch,0.15*inch,fill=1)
    c.rect(5.9*inch,8*inch,1.3*inch,0.15*inch,fill=1)
    c.rect(7.2*inch,8*inch,0.85*inch,0.15*inch,fill=1)

    c.setFillColor("black")
    c.setFont("Times-Bold", 5.5, leading=None)
    c.drawString(5.05*inch, 8.08*inch, "Highest Educational")
    c.drawString(5.2*inch, 8.03*inch, "Attainment")
    c.setFont("Times-Roman", 8, leading=None)
    c.drawString(0.3*inch, 8.02*inch, "Name(Last, First, Middle Name)")
    c.drawString(3.1*inch, 8.02*inch, "Sex")
    c.drawString(3.36*inch, 8.02*inch, "Civil Status")
    c.drawString(4*inch, 8.02*inch, "Relation to Patient")
    
    c.drawString(6.3*inch, 8.02*inch, "Occupation")
    c.drawString(7.25*inch, 8.02*inch, "Monthly Income")
    c.setFillColor(white)
    a =0.15
    b = 7.85
    for i in range(10):
        c.rect(0.25*inch,b*inch,2.8*inch,0.15*inch,fill=1)
        c.rect(3.05*inch,b*inch,0.3*inch,0.15*inch,fill=1)
        c.rect(3.35*inch,b*inch,0.55*inch,0.15*inch,fill=1)
        c.rect(3.9*inch,b*inch,1*inch,0.15*inch,fill=1)
        c.rect(4.9*inch,b*inch,1*inch,0.15*inch,fill=1)
        c.rect(5.9*inch,b*inch,1.3*inch,0.15*inch,fill=1)
        c.rect(7.2*inch,b*inch,0.85*inch,0.15*inch,fill=1)
        b -= a

    famcom = FamilyComposition.objects.filter(uis = uis)
    # count_famcom = FamilyComposition.objects.filter(uis = uis).count()
    pp =0.15
    tt = 7.87
    for cc in famcom:
        c.setFillColor("black")
        c.setFont("Times-Bold", 6.5, leading=None)
        c.drawString(0.27*inch, tt *inch, cc.fullname)
        if cc.gender == 'FEMALE':
            c.drawString(3.15*inch, tt *inch, "F")
        elif cc.gender == 'MALE':
            c.drawString(3.15*inch, tt *inch, "M")
        else:
            c.drawString(3.15*inch, tt *inch, "N/A")
        c.drawString(3.37*inch, tt *inch, cc.cstat)
        c.drawString(3.92*inch, tt *inch, cc.relation_to_patient)
        c.drawString(4.92*inch, tt *inch, cc.hea)
        c.drawString(5.92*inch, tt *inch, cc.occupation)
        famcom_mi = '{:,.2f}'.format(float(cc.mi))
        c.drawString(7.22*inch, tt *inch, famcom_mi)
        tt -=pp

    
        
    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.3*inch, 6.4*inch, "Other Source/s of Family Income")

    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(5.7*inch, 6.1*inch, "Total Family Income")
    c.drawString(5.7*inch, 5.9*inch, "__________________________________________")
    c.drawString(5.72*inch, 5.9*inch,tot_income)

    
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(5.7*inch, 6.1*inch, "Total Family Income")
    ae =0.15
    be = 6.25
    for i in range(4):
        c.drawString(0.3*inch, be*inch, "________________________________________________         __________________________")
        be -= ae
    xe = 0.15
    ye = 6.27
    famcom_osof = Fc_other_source.objects.filter(uis = uis)
    for fo in famcom_osof:
        c.setFont("Times-Bold", 6.5, leading=None)
        c.drawString(0.35*inch, ye*inch, fo.otherSources_of_fi_desc)
        tot_income_osof = '{:,.2f}'.format(float(fo.otherSources_of_fi))
        c.drawString(3.7*inch, ye*inch, tot_income_osof)
        ye -= xe
    list_of_expenses = ListofExpenses.objects.filter(uis = uis)
    for oo in list_of_expenses:
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
    problem_presented = ProblemPresented.objects.filter(uis = uis)
    for mm in problem_presented:
        problem = mm.problem
        conv_problem = problem.replace("[","").replace("]","").replace("'","")
        f_problem = conv_problem.replace(" ","")
        fproblem = f_problem.split(',')
        prob_desc = mm.prob_desc
        conv_prob_desc = prob_desc.replace("[","").replace("]","").replace("'","")
        f_prob_desc = conv_prob_desc.split(',') 
   

    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.68*inch, 5.46*inch, "HOUSE")
    c.drawString(0.68*inch, 5.46*inch, "_______")
    c.drawString(1.7*inch, 5.46*inch, "AMOUNT")
    c.drawString(1.7*inch, 5.46*inch, "_________")

    

    c.setFont("Times-Roman", 8, leading=None)
    c.drawString(2.9*inch, 5.46*inch, "LIGHT SOURCE")
    c.drawString(2.9*inch, 5.46*inch, "_______________")
    c.drawString(3.85*inch, 5.46*inch, "AMOUNT")
    c.drawString(3.85*inch, 5.46*inch, "_________")


    c.setLineWidth(1)
    if fls[0] == 'ELECTRICITY':
        c.setFillColor(black)
        c.rect(2.65*inch,5.30*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(3.62*inch, 5.30*inch, amt_fls[0])
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,5.30*inch,0.09*inch,0.09*inch,fill=1)
    
    if fls[1] == 'KEROSENE':
        c.setFillColor(black)
        c.rect(2.65*inch,5.15*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(3.62*inch, 5.15*inch, amt_fls[1])
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,5.15*inch,0.09*inch,0.09*inch,fill=1)

    if fls[2] == 'CANDLE':
        c.setFillColor(black)
        c.rect(2.65*inch,5*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(3.62*inch, 5*inch, amt_fls[2])
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,5*inch,0.09*inch,0.09*inch,fill=1)

    if fls[3] == 'OTHERS':
        c.setFillColor(black)
        c.rect(2.65*inch,4.85*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(3.62*inch, 4.85*inch, amt_fls[3])
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,4.85*inch,0.09*inch,0.09*inch,fill=1)

    c.setFillColor("black")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(2.8*inch, 5.30*inch, "ELECTRICITY")
    c.drawString(3.6*inch, 5.30*inch, "_________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(2.8*inch, 5.15*inch, "KEROSENE")
    c.drawString(3.6*inch, 5.15*inch, "_________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(2.8*inch, 5*inch, "CANDLE")
    c.drawString(3.6*inch, 5*inch, "_________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(2.8*inch, 4.85*inch, "OTHERS")
    c.drawString(3.6*inch, 4.85*inch, "_________________")

    c.setFont("Times-Roman", 8, leading=None)
    c.drawString(2.9*inch, 4.73*inch, "WATER SOURCE")
    c.drawString(2.9*inch, 4.73*inch, "_______________")
    c.drawString(4*inch, 4.73*inch, "AMOUNT")
    c.drawString(4*inch, 4.73*inch, "_________")

    c.setFillColor("black")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(2.8*inch, 4.58*inch, "PUBLIC")
    c.drawString(3.65*inch, 4.58*inch, "___________________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(2.8*inch, 4.43*inch, "NATURAL")
    c.drawString(3.65*inch, 4.43*inch, "___________________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(2.8*inch, 4.28*inch, "WATER DISTRICT")
    c.drawString(3.65*inch, 4.28*inch, "___________________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(2.8*inch, 4.13*inch, "MINERAL BUY")
    c.drawString(3.65*inch, 4.14*inch, "___________________________")

    c.setLineWidth(1)
    if fws[0] == 'PUBLIC':
        c.setFillColor(black)
        c.rect(2.65*inch,4.58*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(3.7*inch, 4.58*inch, amt_fws[0])
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,4.58*inch,0.09*inch,0.09*inch,fill=1)

    if fws[1] == 'NATURAL':
        c.setFillColor(black)
        c.rect(2.65*inch,4.43*inch,0.1*inch,0.1*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(3.7*inch, 4.43*inch, amt_fws[1])
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,4.43*inch,0.1*inch,0.1*inch,fill=1)

    if fws[2] == 'WATERDISTRICT':
        c.setFillColor(black)
        c.rect(2.65*inch,4.28*inch,0.1*inch,0.1*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(3.7*inch, 4.28*inch, amt_fws[2])
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,4.28*inch,0.1*inch,0.1*inch,fill=1)
    if fws[3] == 'MINERAL':
        c.setFillColor(black)
        c.rect(2.65*inch,4.13*inch,0.1*inch,0.1*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(3.7*inch, 4.13*inch, amt_fws[3])
    else:
        c.setFillColor(white)
        c.rect(2.65*inch,4.13*inch,0.1*inch,0.1*inch,fill=1)

    

    c.setFillColor("black")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.47*inch, 5.30*inch, "OWNED")
    c.drawString(1.57*inch, 5.30*inch, "_________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.47*inch, 5.15*inch, "RENTED")
    c.drawString(1.57*inch, 5.15*inch, "_________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.47*inch, 5*inch, "SHARED")
    c.drawString(1.57*inch, 5*inch, "_________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.47*inch, 4.85*inch, "OTHERS")
    c.drawString(1.57*inch, 4.85*inch, "_________________")
    
   
    c.setLineWidth(1)
    if hauz == 'OWNED': #house
        c.setFillColor(black)
        c.rect(0.3*inch,5.30*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(1.59*inch, 5.30*inch, amt_hauz)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,5.30*inch,0.09*inch,0.09*inch,fill=1)
    if hauz == 'RENTED':
        c.setFillColor(black)
        c.rect(0.3*inch,5.15*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(1.59*inch, 5.15*inch, amt_hauz)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,5.15*inch,0.09*inch,0.09*inch,fill=1)
    
    if hauz == 'SHARED':
        c.setFillColor(black)
        c.rect(0.3*inch,5*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(1.59*inch, 5*inch, amt_hauz)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,5*inch,0.09*inch,0.09*inch,fill=1)
    if hauz == 'OTHERS' or hauz == 'GOVERNMENT' or hauz == 'PRIVATE':
        c.setFillColor(black)
        c.rect(0.3*inch,4.85*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(1.59*inch, 4.85*inch, amt_hauz)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,4.85*inch,0.09*inch,0.09*inch,fill=1)

    c.setFillColor("black")
    c.setFont("Times-Roman", 8, leading=None)
    c.drawString(0.47*inch, 4.73*inch, "LOT")
    c.drawString(0.47*inch, 4.73*inch, "____")

    c.drawString(1.7*inch, 4.73*inch, "AMOUNT")
    c.drawString(1.7*inch, 4.73*inch, "_________")

    c.setFillColor("black")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.47*inch, 4.58*inch, "OWNED")
    c.drawString(1.57*inch, 4.58*inch, "_________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.47*inch, 4.43*inch, "SHARED")
    c.drawString(1.57*inch, 4.43*inch, "_________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.47*inch, 4.28*inch, "GOVERNMENT")
    c.drawString(1.57*inch, 4.28*inch, "_________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.47*inch, 4.13*inch, "PRIVATE PROPERTY")
    c.drawString(1.57*inch, 4.14*inch, "_________________")

    c.setLineWidth(1)
    if lot == 'OWNED': #lot
        c.setFillColor(black)
        c.rect(0.3*inch,4.58*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(1.59*inch, 4.58*inch, amt_lot)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,4.58*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(1.59*inch, 4.58*inch, "-")

    if lot == 'SHARED':
        c.setFillColor(black)
        c.rect(0.3*inch,4.43*inch,0.1*inch,0.1*inch,fill=1)
        c.drawString(1.59*inch, 4.43*inch, amt_lot)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,4.43*inch,0.1*inch,0.1*inch,fill=1)
        c.drawString(1.59*inch, 4.43*inch, "-")
    if lot == 'GOVERNMENT':
        c.setFillColor(black)
        c.rect(0.3*inch,4.28*inch,0.1*inch,0.1*inch,fill=1)
        c.drawString(1.59*inch, 4.28*inch, amt_lot)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,4.28*inch,0.1*inch,0.1*inch,fill=1)
        c.drawString(1.59*inch, 4.28*inch, "-")
    if lot == 'PRIVATE PROPERTY':
        c.setFillColor(black)
        c.rect(0.3*inch,4.13*inch,0.1*inch,0.1*inch,fill=1)
        c.drawString(1.59*inch, 4.13*inch, amt_lot)
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,4.13*inch,0.1*inch,0.1*inch,fill=1)
        c.drawString(1.59*inch, 4.13*inch, "-")

    c.setFillColor("black")
    c.setFont("Times-Roman", 8, leading=None)
    c.drawString(5.45*inch, 5.46*inch, "OTHER EXPENSES")
    c.drawString(5.45*inch, 5.46*inch, "_________________")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(7.2*inch, 5.46*inch, "AMOUNT")
    c.drawString(7.2*inch, 5.46*inch, "_________")

    c.setLineWidth(1)
    if oe[0] == 'HOUSE':
        c.setFillColor(black)
        c.rect(5*inch,5.30*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 5.30*inch, amt_oe[0])
    else:
        c.setFillColor(white)
        c.rect(5*inch,5.30*inch,0.09*inch,0.09*inch,fill=1)
    
    if oe[3] == 'EDU':
        c.setFillColor(black)
        c.rect(5*inch,5.15*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 5.15*inch, amt_oe[3])
    else:
        c.setFillColor(white)
        c.rect(5*inch,5.15*inch,0.09*inch,0.09*inch,fill=1)
    if oe[6] == 'FOOD':
        c.setFillColor(black)
        c.rect(5*inch,5*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 5*inch, amt_oe[6])
    else:
        c.setFillColor(white)
        c.rect(5*inch,5*inch,0.09*inch,0.09*inch,fill=1)

    if oe[1] == 'ME':
        c.setFillColor(black)
        c.rect(5*inch,4.85*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 4.85*inch, amt_oe[1])
    else:
        c.setFillColor(white)
        c.rect(5*inch,4.85*inch,0.09*inch,0.09*inch,fill=1)

    if oe[4] == 'LOAN':
        c.setFillColor(black)
        c.rect(5*inch,4.7*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 4.7*inch, amt_oe[4])
    else:
        c.setFillColor(white)
        c.rect(5*inch,4.7*inch,0.09*inch,0.09*inch,fill=1)

    if oe[7] == 'SAVINGS':
        c.setFillColor(black)
        c.rect(5*inch,4.55*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 4.55*inch, amt_oe[7])
    else:
        c.setFillColor(white)
        c.rect(5*inch,4.55*inch,0.09*inch,0.09*inch,fill=1)

    if oe[2] == 'IP':
        c.setFillColor(black)
        c.rect(5*inch,4.4*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 4.4*inch, amt_oe[2])
    else:
        c.setFillColor(white)
        c.rect(5*inch,4.4*inch,0.09*inch,0.09*inch,fill=1)
    if oe[5] == 'TRANSPO':
        c.setFillColor(black)
        c.rect(5*inch,4.25*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 4.25*inch, amt_oe[5])
    else:
        c.setFillColor(white)
        c.rect(5*inch,4.25*inch,0.09*inch,0.09*inch,fill=1)

    if oe[8] == 'OTHER':
        c.setFillColor(black)
        c.rect(5*inch,4.12*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 7, leading=None)
        c.drawString(6.73*inch, 4.12*inch, amt_oe[8])
    else:
        c.setFillColor(white)
        c.rect(5*inch,4.12*inch,0.09*inch,0.09*inch,fill=1)


    c.setFillColor("black")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(5.2*inch, 5.30*inch, "HOUSEHELP")
    c.drawString(6.7*inch, 5.30*inch, "___________________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(5.2*inch, 5.15*inch, "EDUCATION")
    c.drawString(6.7*inch, 5.15*inch, "___________________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(5.2*inch, 5*inch, "FOOD")
    c.drawString(6.7*inch, 5*inch, "___________________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(5.2*inch, 4.85*inch, "MEDICAL EXPENDITURES")
    c.drawString(6.7*inch, 4.85*inch, "___________________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(5.2*inch, 4.7*inch, "LOAN")
    c.drawString(6.7*inch, 4.7*inch, "___________________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(5.2*inch, 4.55*inch, "SAVINGS")
    c.drawString(6.7*inch, 4.55*inch, "___________________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(5.2*inch, 4.4*inch, "INSURANCE PREMIUM")
    c.drawString(6.7*inch, 4.4*inch, "___________________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(5.2*inch, 4.25*inch, "TRANSPORTATION")
    c.drawString(6.7*inch, 4.25*inch, "___________________________")

    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(5.2*inch, 4.12*inch, "OTHERS")
    c.drawString(6.7*inch, 4.12*inch, "___________________________")

    c.setFillColor("black")
    c.setFont("Times-Bold", 6.5, leading=None)
    c.drawString(0.27*inch, 3.92*inch, "Problem Presented")

    c.setLineWidth(1)
    if fproblem[0] == 'HCOP':
        c.setFillColor(black)
        c.rect(0.3*inch,3.75*inch,0.09*inch,0.09*inch,fill=1)
        # c.setFont("Times-Bold", 5, leading=None)
        # c.drawString(2.23*inch, 3.75*inch,f_prob_desc[0])
        
        p = Paragraph(f_prob_desc[0], style=custom_font_size)
        p.wrapOn(c, 110,20)  
        p.drawOn(c,2.23*inch,3.75*inch) 
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,3.75*inch,0.09*inch,0.09*inch,fill=1)

    if fproblem[1] == 'FN':
        c.setFillColor(black)
        c.rect(0.3*inch,3.6*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 5, leading=None)
        c.drawString(2.23*inch, 3.6*inch,f_prob_desc[1])
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,3.6*inch,0.09*inch,0.09*inch,fill=1)

    if fproblem[2] == 'EMP':
        c.setFillColor(black)
        c.rect(0.3*inch,3.45*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 5, leading=None)
        c.drawString(2.23*inch, 3.45*inch,f_prob_desc[2])
    else:
        c.setFillColor(white)
        c.rect(0.3*inch,3.45*inch,0.09*inch,0.09*inch,fill=1)

    c.setFillColor("black")
    c.setFont("Times-Roman", 6, leading=None)
    c.drawString(0.47*inch, 3.75*inch, "HEALTH CONDITION OF PATIENT(specify)")
    c.drawString(2.2*inch, 3.75*inch, "_____________________________________")
    c.drawString(0.47*inch, 3.6*inch, "FOOD/NUTRITION(specify)")
    c.drawString(2.2*inch, 3.6*inch, "_____________________________________")
    c.drawString(0.47*inch, 3.45*inch, "EMPLOYMENT(specify)")
    c.drawString(2.2*inch, 3.45*inch, "_____________________________________")

    c.setLineWidth(1)
    if fproblem[3] == 'ERS':
        c.setFillColor(black)
        c.rect(3.8*inch,3.75*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 5, leading=None)
        c.drawString(5.28*inch, 3.75*inch,f_prob_desc[3])
    else:
        c.setFillColor(white)
        c.rect(3.8*inch,3.75*inch,0.09*inch,0.09*inch,fill=1)

    if fproblem[4] == 'HS': 
        c.setFillColor(black)
        c.rect(3.8*inch,3.6*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 5, leading=None)
        c.drawString(5.28*inch, 3.6*inch,f_prob_desc[4])
    else:
        c.setFillColor(white)
        c.rect(3.8*inch,3.6*inch,0.09*inch,0.09*inch,fill=1)
        
    
    if fproblem[5] == 'OSY':
        c.setFillColor(black)
        c.rect(3.8*inch,3.45*inch,0.09*inch,0.09*inch,fill=1)
        c.setFont("Times-Bold", 5, leading=None)
        c.drawString(5.28*inch, 3.45*inch,f_prob_desc[5])
    else:
        c.setFillColor(white)
        c.rect(3.8*inch,3.45*inch,0.09*inch,0.09*inch,fill=1)

    c.setFillColor(white)#thumbmark
    c.rect(6.8*inch,2.6*inch,1.2*inch,1.3*inch,fill=1)

    c.setFillColor("black")
    c.setFont("Times-Roman", 6, leading=None)
    c.drawString(3.95*inch, 3.75*inch, "ECONOMIC RESOURCES(specify)")
    c.drawString(5.25*inch, 3.75*inch, "___________________________________")
    c.drawString(3.95*inch, 3.6*inch, "HOUSING(specify)")
    c.drawString(5.25*inch, 3.6*inch, "___________________________________")
    c.drawString(3.95*inch, 3.45*inch, "Others(specify)")
    c.drawString(5.25*inch, 3.45*inch, "___________________________________")
    c.setFont("Times-Roman", 7, leading=None)
    c.drawString(0.3*inch, 3.25*inch, "AKO SI _______________________________________________________ AY NAGPAPATUNAY NA ANG MGA IMPORMASYONG NAKASULAT")
    c.drawString(0.3*inch, 3.15*inch, "SA IBABAW AY TOTOO AT TAMA. PINAPAHINTULUTAN KO DIN MAIBAHAGI ANG MGA NATURANG IMPORMASYON SA IBA PANG")
    c.drawString(0.3*inch, 3.05*inch, "AHENSIYA NG GOBYERNO PARA SA ANUMANG NAAANGKOP NA PAG GAMIT.")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.68*inch, 3.27*inch, informant_fullname)

    c.drawString(2*inch, 2.6*inch, "_____________________________________________________________________")
    c.setFont("Times-Roman", 6, leading=None)
    c.drawString(2.6*inch, 2.5*inch, "Name and Signature of client (PAngalan at lagda ng Kliyente)")
    c.setFont("Times-Bold", 7, leading=None)
    
    
    text_width = c.stringWidth(informant_fullname)/100
    input_width = 242/100
    center_x = (input_width - text_width) / 2
    f_center_x = center_x + 2.02
    c.drawString(f_center_x*inch, 2.62*inch, informant_fullname)
    
    # if len(examp) >= 167:
    #     c.setFont("Times-Bold", 7.5, leading=None)
    #     c.drawString(0.3*inch, 2.2*inch, examp[:167])
    #     c.drawString(0.3*inch, 2.1*inch, examp[167:334])
    #     c.drawString(0.3*inch, 2*inch, examp[334:501])
    #     c.drawString(0.3*inch, 1.9*inch, examp[501:668])
    #     c.drawString(0.3*inch, 1.8*inch, examp[668:835])
    #     c.drawString(0.3*inch, 1.7*inch, examp[835:1002])
    #     c.drawString(0.3*inch, 1.6*inch, examp[1002:1169])
    #     c.drawString(0.3*inch, 1.5*inch, examp[1169:1336])

    swa_desc = SWA.objects.filter(uis = uis)
    for sw in swa_desc:
        desc_swa = sw.swa_desc
        p = Paragraph(desc_swa, style=custom_font_size_swa )
        p.wrapOn(c, 540,20)  
        p.drawOn(c,0.3*inch,1.53*inch) 

    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(0.25*inch,1.2*inch,2.8*inch,0.15*inch,fill=1)
    c.rect(3.05*inch,1.2*inch,1.4*inch,0.15*inch,fill=1)
    c.rect(4.45*inch,1.2*inch,2*inch,0.15*inch,fill=1)
    c.rect(6.45*inch,1.2*inch,1.6*inch,0.15*inch,fill=1)

    c.setFillColor("black")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(1*inch, 1.22*inch, "TYPE OF ASSISTANCE")
    c.drawString(3.14*inch, 1.22*inch, "AMOUNT OF ASSISTANCE")
    c.drawString(4.9*inch, 1.22*inch, "MODE OF ASSISTANCE")
    c.drawString(6.9*inch, 1.22*inch, "FUND SOURCE")

    x = 0.12
    y = 1.08
    for i in range(5):
        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(0.25*inch,y*inch,2.8*inch,0.12*inch,fill=1)
        c.rect(3.05*inch,y*inch,1.4*inch,0.12*inch,fill=1)
        c.rect(4.45*inch,y*inch,2*inch,0.12*inch,fill=1)
        c.rect(6.45*inch,y*inch,1.6*inch,0.12*inch,fill=1)
        y -= x

    reccom = Recommendations.objects.filter(uis = uis)
    # count_famcom = FamilyComposition.objects.filter(uis = uis).count()
    ll =0.12
    zz = 1.1
    for bb in reccom:
        c.setFillColor("black")
        c.setFont("Times-Bold", 6.5, leading=None)
        c.drawString(0.27*inch, zz *inch, bb.type_of_assistance)
        amt_assist = '{:,.2f}'.format(float(bb.amt_of_assistance))
        c.drawString(3.1*inch, zz *inch, amt_assist)
        c.drawString(4.49*inch, zz *inch, bb.mode_of_assistance)
        c.drawString(6.49*inch, zz *inch, bb.fund_source)
      
        zz -=ll
    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(0.25*inch,0.25*inch,1.3*inch,0.3*inch,fill=1)
    c.rect(1.55*inch,0.25 *inch,2.5*inch,0.2*inch,fill=1)
    c.rect(4.05*inch,0.25 *inch,1.5*inch,0.3*inch,fill=1)
    c.rect(5.55*inch,0.25 *inch,2.5*inch,0.2*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Bold", 7, leading=None)
    
    user_width = c.stringWidth("request.session['name']")/100
    user_input_width = 180/100
    center_user = (user_input_width - user_width) / 2
    f_center_user_x = center_user + 1.57
    c.drawString(f_center_user_x*inch, 0.35*inch, request.session['name'] +", "+ str("RSW"))
    c.setFillColor("black")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.5*inch, 0.35*inch, "Interviewed by:")
    c.drawString(4.2*inch, 0.35*inch, "Reviewed and Approved by:")
    c.drawString(5.73*inch, 0.35*inch, "MARIA JEZEBEL F. DE MESA, RSW, MAEd-GC")
    c.setFont("Times-Bold", 5, leading=None)
    c.drawString(6.2*inch, 0.28*inch, "SOCIAL WELFARE OFFICER III")
    # c.drawString(2.4*inch, 0.28*inch, "Social Worker Officer")

    uw = c.stringWidth(request.session['position'])/100
    uiw = 180/100
    cu = (uiw - uw) / 2
    fxi = cu+ 1.75
    c.drawString(fxi*inch, 0.28*inch, request.session['position'])

    # counttt = c.stringWidth("FOR CONSULTATIONBOV both eyesVA: OD   20/50+2         PH: OD   20/32         OS: 20/200          OS: NIw/Cor: OD   20/40                   NCT: OD  30.9           OS: 20/200                OS: 46.3")
    # print(counttt)
    
    c.showPage()
    c.save()
    pdf = buf.getvalue()
    buf.close()
    response.write(pdf)
    return response



