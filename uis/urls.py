from django.urls import path
# from . import uis_pdf, views , new_mssat, mssat,psyco_profile
from django.conf import settings
from django.conf.urls.static import static
from .views import views, add_uis, walkin_uis,exceltoweb_uis,add_uis_new,del_actions,mssat_list,social_profile,scp
from . import uis_pdf,new_mssat,psyco_profile


urlpatterns = [
    path('', views.home, name='home'),
    path('auth_login', views.auth_login, name='auth_login'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('<str:hospno>/get_patient_enctr/',views.get_patient_enctr,name='get_patient_enctr'),
    path('<str:hospno>/<str:code>/<str:toecode>/get_patient_history/',add_uis.get_patient_history,name='get_patient_history'),
    path('<str:uis>/<str:hospno>/get_patient_uis_to_mssat/',mssat_list.get_patient_uis_to_mssat,name='get_patient_uis_to_mssat'),
    path('<str:uis>/<str:hospno>/get_patient_uis_to_mssat_history/',mssat_list.get_patient_uis_to_mssat_history,name='get_patient_uis_to_mssat_history'),
    path('<str:hospno>/<str:code>/<str:toecode>/add_uis/', add_uis.add_uis, name='add_uis'),
    path('uis_list', views.uis_list, name='uis_list'),
    path('admitted_list', views.admitted_list, name='admitted_list'),
    path('report', views.report, name='report'),
    path('uis_excel', exceltoweb_uis.uis_excel, name='uis_excel'),
    path('<str:named>/exceltoweb_uis/', exceltoweb_uis.exceltoweb_uis, name='exceltoweb_uis'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('walkin_uis', walkin_uis.walkin_uis, name='walkin_uis'),
    path('copy_uis_add', add_uis.copy_uis_add, name='copy_uis_add'),
    # path('process_duplicate_uis', views.process_duplicate_uis, name='process_duplicate_uis'),
    path('walkin_page', walkin_uis.walkin_page, name='walkin_page'),
    path('<str:uis>/<str:uis_miscs>/<str:mssats>/get_patient_scp_history', scp.get_patient_scp_history, name='get_patient_scp_history'),
    path('<str:uis>/<str:uis_miscs>/<str:mssats>/add_scp', scp.add_scp, name='add_scp'),
    path('<str:scp>/<str:mssat>/process_edit_scp', scp.process_edit_scp, name='process_edit_scp'),
    path('<str:mssat>/edit_scp', scp.edit_scp, name='edit_scp'),
    path('<str:uis>/<str:uis_misc>/update_uis', add_uis_new.update_uis, name='update_uis'),
    path('<str:uis>/<str:uis_misc>/edit_uis', add_uis_new.edit_uis, name='edit_uis'),
    path('<str:uis>/<str:uis_misc>/copy_uis', add_uis.copy_uis, name='copy_uis'),
    # path('<str:uis>/duplicate_uis', views.duplicate_uis, name='duplicate_uis'),
    path('<str:uis>/<str:uis_misc>/process_edit_uis', add_uis_new.process_edit_uis, name='process_edit_uis'),
    path('<str:uis>/process_update_uis', add_uis_new.process_update_uis, name='process_update_uis'),
    path('<str:uis>/<str:misc_uis>/add_mssat', mssat_list.add_mssat, name='add_mssat'),
    #  path('<str:uis>/<str:uis_misc>/add_uis_mssat', mssat_list.add_uis_mssat, name='add_uis_mssat'),
    path('mss_tool_list', views.mss_tool_list, name='mss_tool_list'),
    path('social_profile', social_profile.social_profile, name='social_profile'),
    path('<str:uis>/<str:uis_misc>/uis_pdf', uis_pdf.uis_pdf, name='uis_pdf'),
    # path('<str:uis>/mssat_pdf', mssat.mssat_pdf, name='mssat_pdf'),
    path('<str:uis>/<str:uis_misc>/new_mssat_pdf', new_mssat.new_mssat_pdf, name='new_mssat_pdf'),
    path('<str:uis_id>/<str:reccom_id>/<str:uis_misc>/del_reccom', del_actions.del_reccom, name='del_reccom'),
    path('<str:uis_id>/<str:osof_id>/<str:uis_misc>/del_famcom_osof', del_actions.del_famcom_osof, name='del_famcom_osof'),
    path('<str:uis_id>/<str:famcom_id>/<str:uis_misc>/del_famcom', del_actions.del_famcom, name='del_famcom'),
    path('<str:mssat>/update_msstool', mssat_list.update_msstool, name='update_msstool'),
    path('<str:mssat>/process_update_mssat', mssat_list.process_update_mssat, name='process_update_mssat'),
    path('add_uis_excel/', exceltoweb_uis.add_uis_excel, name='add_uis_excel'),
    # path('<str:uis_id>/delete_uis/' ,views.delete_uis, name ='delete_uis'),
    path('<str:scp_tab_id>/<str:mssat>/delete_scp_tab/' ,del_actions.delete_scp_tab, name ='delete_scp_tab'),
    path('<str:uis_id>/<str:uis_misc>/<str:mssats>/psycoProfile/', psyco_profile.psycoProfile, name='psycoProfile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)