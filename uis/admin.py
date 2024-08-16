from django.contrib import admin
from . models import UIS,Informant,IdentifyingInformation,FamilyComposition,ListofExpenses,ProblemPresented,SWA,Recommendations



admin.site.site_header = "UNIFIED INTAKE SHEET SYSTEM"
admin.site.index_title ="WELCOME ADMINISTRATOR"

class UisAdmin(admin.ModelAdmin):
    list_display =['uis','date']
    search_fields =['uis','date']
class InformantAdmin(admin.ModelAdmin):
    list_display =['date_of_intake','fullname']
    search_fields =['date_of_intake','fullname']
class IdentifyingInformationAdmin(admin.ModelAdmin):
    list_display = ['uis','client_name']
    search_fields = ['uis','client_name']
class FamilyCompositionAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'relation_to_patient']
    search_fields = ['fullname', 'relation_to_patient']
class ListofExpensesAdmin(admin.ModelAdmin):
    list_display = ['uis','listofExpenses']
    search_fields = ['uis','listofExpenses']
class ProblemPresentedAdmin(admin.ModelAdmin):
    list_display = ['problemPresented','problem']
    search_fields = ['problemPresented','problem']
class SwaAdmin(admin.ModelAdmin):
    list_display = ['swa']
    search_fields = ['swa']
class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ['recommendation']
    search_fields = ['recommendation']
    

admin.site.register(UIS, UisAdmin)
admin.site.register(Informant, InformantAdmin)
admin.site.register(IdentifyingInformation, IdentifyingInformationAdmin)
admin.site.register(FamilyComposition,FamilyCompositionAdmin)
admin.site.register(ListofExpenses,ListofExpensesAdmin)
admin.site.register(ProblemPresented,ProblemPresentedAdmin)
admin.site.register(SWA,SwaAdmin)
admin.site.register(Recommendations,RecommendationsAdmin)

