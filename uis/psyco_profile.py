from django.shortcuts import render,get_object_or_404,reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, FileResponse
from django.core.exceptions import ObjectDoesNotExist
from reportlab.pdfgen import canvas
import io
from reportlab.lib.colors import blue, gray, whitesmoke,white,black
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from datetime import date, datetime, time
from uis.models import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

def psycoProfile(request,uis_id, uis_misc,mssats):
    padaba = 'uis/static/padabrghgmc.png'
    logo = 'uis/static/logo.png'
    doh_logo = 'uis/static/doh.png'
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    response = HttpResponse(content_type='application/pdf')
    c.setTitle("PSYCO PROFILE")
    c.setPageSize((8.27*inch, 11.69*inch))
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
    c.setLineWidth(2)
    c.line(0.25*inch,10.55*inch,8*inch,10.55*inch)
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    custom_font_size_swa = style.clone('CustomStyle')
    custom_font_size_swa_first = style.clone('CustomStyle')
    custom_font_size_swa.fontSize = 6.5
    custom_font_size_swa.leading = 6.5

    c.setFillColor("black")# MEDICAL SOCIAL WORK DEPARTMENT
    c.setFont("Times-Roman", 12, leading=None)
    c.drawString(2.6*inch, 10.4*inch, "MEDICAL SOCIAL WORK DEPARTMENT")
    now = datetime.now()
    date_today = datetime.strftime(now, '%B %d, %Y')
    c.setFillColor("black")
    c.setFont("Times-Bold", 12, leading=None)
    c.drawString(2.92*inch, 10*inch, "Social Profile with Social Care Plan")
    get_details = UIS.objects.filter(uis = uis_id)
    for i in get_details:
        hospno = i.hospno
    get_misc = UIS_misc.objects.filter(uis_misc = uis_misc)
    for r in get_misc:
        mswd_cat = r.category

    mssat = MSSAT.objects.filter(uis = uis_id,uis_misc=uis_misc)
    for sc in mssat:
        ward = sc.basic_ward
        mss_no =sc.mss_no
 
    iden_info = IdentifyingInformation.objects.filter(uis=uis_id)
    for ii in iden_info:
        fullname = ii.client_name
    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(0.25*inch, 9.3*inch, "Health Record No:")

    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(1.35*inch, 9.3*inch, "_______________________________________")
    c.drawString(1.4*inch, 9.3*inch, hospno)

    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(0.77*inch, 9.1*inch, "MSS No:")

    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(1.35*inch, 9.1*inch, "_______________________________________")
    c.drawString(1.4*inch, 9.1*inch, mss_no)

    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(6.5*inch, 9.55*inch, "Date")
    uw = c.stringWidth(date_today)/100
    uiw = 120/100
    cu = (uiw - uw) / 2
    fxi = cu + 5.8
 
    c.setFillColor("black")
    c.setFont("Times-Roman", 12, leading=None)
    c.drawString(5.5*inch, 9.7*inch, "___________________________")
    c.drawString(fxi*inch, 9.7*inch, date_today)

    c.setFillColor("black")
    c.setFont("Times-Bold", 10, leading=None)
    c.drawString(0.25*inch, 8.7*inch, "I. Patient's Name:   ____________________________________________________________________________________________")
    c.drawString(1.45*inch, 8.7*inch, fullname)
    c.setFillColor("black")
    c.setFont("Times-Bold", 10, leading=None)
    c.drawString(0.25*inch, 8.5*inch, "II. Ward:                               IP                                 ER                            OPD")

    c.setLineWidth(1)
    
    if ward == 'ER':
        c.setFillColor(black)#ER
        c.rect(2.96*inch,8.5*inch,0.1*inch,0.1*inch,fill=1)
        c.setFillColor(white)#OPD
        c.rect(4.1*inch,8.5*inch,0.1*inch,0.1*inch,fill=1)
        c.setFillColor(white)#IP
        c.rect(1.7*inch,8.5*inch,0.1*inch,0.1*inch,fill=1)
    elif ward =='OPD':
        c.setFillColor(black)#OPD
        c.rect(4.1*inch,8.5*inch,0.1*inch,0.1*inch,fill=1)
        c.setFillColor(white)#ER
        c.rect(2.96*inch,8.5*inch,0.1*inch,0.1*inch,fill=1)
        c.setFillColor(white)#IP
        c.rect(1.7*inch,8.5*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(black)#IP
        c.rect(1.7*inch,8.5*inch,0.1*inch,0.1*inch,fill=1)
        c.setFillColor(white)#OPD
        c.rect(4.1*inch,8.5*inch,0.1*inch,0.1*inch,fill=1)
        c.setFillColor(white)#ER
        c.rect(2.96*inch,8.5*inch,0.1*inch,0.1*inch,fill=1)

    c.setFillColor("black")
    c.setFont("Times-Bold", 10, leading=None)
    c.drawString(0.25*inch, 8.3*inch, "III. Classification:")

    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(1*inch,7.8*inch,2.2*inch,0.3*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(1.3*inch, 7.9 *inch, "Financially Capable/Capacitated")
    if mswd_cat == 'C1':
        c.setFillColor(black)#FC
        c.rect(1.1*inch,7.9*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(white)#FC
        c.rect(1.1*inch,7.9*inch,0.1*inch,0.1*inch,fill=1)
    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(3.2*inch,7.8*inch,2.3*inch,0.3*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(3.45*inch, 7.9 *inch, "Financially Incapable/Incapacitated")
    if mswd_cat == 'C2' or mswd_cat == 'C3':
        c.setFillColor(black)#IFC
        c.rect(3.3*inch,7.9*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(white)#IFC
        c.rect(3.3*inch,7.9*inch,0.1*inch,0.1*inch,fill=1)
    

    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(5.5*inch,7.8*inch,0.5*inch,0.3*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(5.8*inch, 7.9 *inch, "C1")
    if mswd_cat == 'C1':
        c.setFillColor(black)#C1
        c.rect(5.6*inch,7.9*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(white)#C1
        c.rect(5.6*inch,7.9*inch,0.1*inch,0.1*inch,fill=1)
   

    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(6*inch,7.8*inch,0.5*inch,0.3*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(6.3*inch, 7.9 *inch, "C2")
    if mswd_cat == 'C2':
        c.setFillColor(black)#C2
        c.rect(6.1*inch,7.9*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(white)#C2
        c.rect(6.1*inch,7.9*inch,0.1*inch,0.1*inch,fill=1)

    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(6.5*inch,7.8*inch,0.5*inch,0.3*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(6.8*inch, 7.9 *inch, "C3")
    if mswd_cat == 'C3':
        c.setFillColor(black)#C3
        c.rect(6.6*inch,7.9*inch,0.1*inch,0.1*inch,fill=1)
    else:
        c.setFillColor(white)#C3
        c.rect(6.6*inch,7.9*inch,0.1*inch,0.1*inch,fill=1)

    c.setFillColor("black")
    c.setFont("Times-Bold", 10, leading=None)
    c.drawString(0.25*inch, 7.5*inch, "IV. Psychosocial Assessment:")

    c.setFillColor(white)#C3
    c.rect(0.3*inch,6.2*inch,7.7*inch,1.2*inch,fill=1)

    # swa_desc = SWA.objects.filter(uis = uis_id,uis_misc=uis_misc)
    psycho_assessment = SCP.objects.filter(uis = uis_id,uis_misc=uis_misc,mssat=mssats)
    for sw in psycho_assessment:
        desc_swa = sw.psychosocial_assessment
        scp_id = sw.scp
        p = Paragraph(desc_swa, style=custom_font_size_swa )
        p.wrapOn(c, 550,20)  
        p.drawOn(c,0.33*inch,6.25*inch) 
    c.setFillColor("black")
    c.setFont("Times-Bold", 10, leading=None)
    c.drawString(0.25*inch, 5.8*inch, "V. Social Care Plan:")

    c.setFillColor(white)#C3
    c.rect(0.3*inch,5.5*inch,7.7*inch,0.25*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Bold", 8, leading=None)
    c.drawString(0.8*inch, 5.58*inch, "Area 1 - Health / Treatment ; 2 - Psychosocial Assessment ; 3 - Affectional Support System ; 4 - Basic Needs (Financial / Housing / Clothing)")

    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(0.3*inch,5.25*inch,0.4*inch,0.25*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Bold", 10, leading=None)
    c.drawString(0.34*inch, 5.35*inch, "Area")

    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(0.7*inch,5.25*inch,1.4*inch,0.25*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(1*inch, 5.35*inch, "Problem/Needs")

    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(2.1*inch,5.25*inch,1.5*inch,0.25*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(2.3*inch, 5.35*inch, "Goals/Objectives")

    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(3.6*inch,5.25*inch,1*inch,0.25*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(3.65*inch, 5.39*inch, "Treatment/")
    c.drawString(3.65*inch, 5.28*inch, "Interventions")

    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(4.6*inch,5.25*inch,1.5*inch,0.25*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(4.65*inch, 5.32*inch, "Frequency/Durations")

    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(6.1*inch,5.25*inch,1*inch,0.25*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(6.15*inch, 5.39*inch, "Responsible")
    c.drawString(6.15*inch, 5.28*inch, "Person")

    c.setLineWidth(1)
    c.setFillColor(white)
    c.rect(7.1*inch,5.25*inch,0.9*inch,0.25*inch,fill=1)
    c.setFillColor("black")
    c.setFont("Times-Roman", 10, leading=None)
    c.drawString(7.15*inch, 5.39*inch, "Expected")
    c.drawString(7.15*inch, 5.28*inch, "Person")

    
    a = 4.75
    b = 0.5
    for i in range(5):
        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(0.3*inch,a*inch,0.4*inch,0.5*inch,fill=1)

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(0.7*inch,a*inch,1.4*inch,0.5*inch,fill=1)

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(2.1*inch,a*inch,1.5*inch,0.5*inch,fill=1)

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(3.6*inch,a*inch,1*inch,0.5*inch,fill=1)

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(4.6*inch,a*inch,1.5*inch,0.5*inch,fill=1)

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(6.1*inch,a*inch,1*inch,0.5*inch,fill=1)

        c.setLineWidth(1)
        c.setFillColor(white)
        c.rect(7.1*inch,a*inch,0.9*inch,0.5*inch,fill=1)
        a-=b
    scp_tab = scp_table.objects.filter(scp = scp_id)
    ll =4.77
    zz = 0.5
    for bb in scp_tab:
        c.setFillColor("black")
        c.setFont("Times-Bold", 10, leading=None)
        c.drawString(0.47*inch, ll *inch, bb.area)
        c.setFont("Times-Bold", 7.5, leading=None)
        # c.drawString(0.72*inch, ll *inch, )
        p = Paragraph(bb.problem_need, style=custom_font_size_swa )
        p.wrapOn(c, 98,50)  
        p.drawOn(c,0.72*inch,ll*inch) 
        # c.drawString(2.12*inch, ll *inch, bb.goals_objective)
        p = Paragraph(bb.goals_objective, style=custom_font_size_swa )
        p.wrapOn(c, 98,50)  
        p.drawOn(c,2.12*inch,ll*inch) 
        # c.drawString(3.62*inch, ll *inch, bb.treatment_intervention)
        p = Paragraph(bb.treatment_intervention, style=custom_font_size_swa )
        p.wrapOn(c, 70,50)  
        p.drawOn(c,3.62*inch,ll*inch) 
        # c.drawString(4.62*inch, ll *inch, bb.frequency_duration)
        p = Paragraph(bb.frequency_duration, style=custom_font_size_swa )
        p.wrapOn(c, 98,50)  
        p.drawOn(c,4.62*inch,ll*inch) 
        # c.drawString(6.12*inch, ll *inch, bb.responsible_person)
        p = Paragraph(bb.responsible_person, style=custom_font_size_swa )
        p.wrapOn(c, 70,50)  
        p.drawOn(c,6.12*inch,ll*inch) 
        # c.drawString(7.12*inch, ll *inch, bb.expected_output)
        p = Paragraph(bb.expected_output, style=custom_font_size_swa )
        p.wrapOn(c, 65,50)  
        p.drawOn(c,7.12*inch,ll*inch) 
        ll -=zz

    c.setFillColor("black")
    c.setFont("Times-Bold", 10, leading=None)
    c.drawString(0.25*inch, 2.5*inch, "VI. Recommendation for Other Team Members:")

    c.setFillColor(white)#C3
    c.rect(0.3*inch,1.9*inch,7.7*inch,0.5*inch,fill=1)

    rot_m = SCP.objects.filter(uis = uis_id,uis_misc=uis_misc,mssat=mssats)
    for s in rot_m:
        if s.reccomendation_for_oth_member == 'ELIGIBLE':
            show = "ELIGIBLE TO AVAIL ASSISTANCE IN MALASAKIT CENTER"
        else:
            show = s.reccomendation_for_oth_member
        p = Paragraph(show, style=custom_font_size_swa )
        p.wrapOn(c, 550,20)  
        p.drawOn(c,0.33*inch,1.93*inch) 

    c.setFillColor("black")
    c.setFont("Times-Bold", 7, leading=None)
    c.drawString(0.3*inch, 1.75*inch, "Prepared by:")
    c.drawString(0.3*inch, 1*inch, "Noted by:")
    c.drawString(0.3*inch, 0.7*inch, "MARIA JEZEBEL F. DE MESA, RSW, MAEd-GC")
    c.setFont("Times-Bold", 5, leading=None)
    c.drawString(0.8*inch, 0.6*inch, "SOCIAL WELFARE OFFICER III")

    c.setFillColor("black")
    c.setFont("Times-Bold", 7, leading=None)
    user_width = c.stringWidth("request.session['name']")/100
    user_input_width = 180/100
    center_user = (user_input_width - user_width) / 2
    f_center_user_x = center_user + 0.2
    c.drawString(f_center_user_x*inch, 1.35*inch, request.session['name'] +", "+ str("RSW"))

    c.setFont("Times-Bold", 5, leading=None)
    uw = c.stringWidth(request.session['position'])/100
    uiw = 180/100
    cu = (uiw - uw) / 2
    fxi = cu+ 0.35
    c.drawString(fxi*inch, 1.25*inch, request.session['position'])

    c.setFillColor("black")
    c.line(0, 0.35*inch, 800, 0.35*inch) #(x1, y1, x2, y2)
    c.setFont("Times-Italic", 10, leading=None)
    c.drawString(0.77*inch, 0.20*inch, "BRGHGMC-F-HOPSS-EFM-003")
    c.drawString(3.2*inch, 0.20*inch, "Rev 2")
    c.drawString(4.7*inch, 0.20*inch, "Effectivity Date: May 2, 2023")
    c.drawImage(padaba, 6.6*inch, 0.06*inch, mask='auto', width=100, height=20)
    
    c.showPage()
    c.save()
    pdf = buf.getvalue()
    buf.close()
    response.write(pdf)
    return response
