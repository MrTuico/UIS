from django.db import models
import uuid

class UIS_copy(models.Model):
    uis_copy = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    uis_excel = models.FileField(upload_to = "")
    def __str__(self):
        return f"{self.uis_copy}"

class UIS(models.Model):
    uis = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    hospno = models.CharField(max_length=30)
    phil_no = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    total_income = models.CharField(max_length=20, default=0)
    total_expense = models.CharField(max_length=20, default = 0)
    category = models.CharField(max_length=10,default='?')
    householdsize = models.CharField(max_length=5,default=0)
    has_scsr = models.BooleanField(default=False)
    has_mssat = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.uis}"


class Informant(models.Model):
    informant = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    uis = models.ForeignKey(UIS,on_delete=models.CASCADE)
    date_of_intake =  models.CharField(max_length=20)
    fullname =  models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    time_of_interview = models.CharField(max_length=15)
    end_time_of_interview = models.CharField(max_length=15,default="12:00")
    relation_to_patient = models.CharField(max_length =50)
    contact_number = models.CharField(max_length = 30)
    def __str__(self):
        return f"{self.informant}"
class IdentifyingInformation(models.Model):
    identifyingInformation = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    uis = models.ForeignKey(UIS,on_delete=models.CASCADE)
    client_name =  models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    dob = models.CharField(max_length = 50)
    age = models.CharField(max_length = 3)
    pob = models.CharField(max_length = 150)
    permanent_address = models.CharField(max_length = 150)
    present_address = models.CharField(max_length = 150)
    cstat = models.CharField(max_length=10)
    religion = models.CharField(max_length=15)
    nationality = models.CharField(max_length=20)
    hea = models.CharField(max_length=15)
    occupation = models.CharField(max_length=20)
    mi = models.CharField(max_length=10)
    patient_type = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.identifyingInformation}"
class FamilyComposition(models.Model):
    familyComposition = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    uis = models.ForeignKey(UIS,on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50)
    age = models.CharField(max_length = 3,default=0)
    gender = models.CharField(max_length=10)
    cstat = models.CharField(max_length=10)
    relation_to_patient = models.CharField(max_length=10)
    hea= models.CharField(max_length=20)
    occupation = models.CharField(max_length=20)
    mi = models.CharField(max_length=15)
    
    
    def __str__(self):
        return f"{self.familyComposition}"
class Fc_other_source(models.Model):
    fc_other_source= models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    uis = models.ForeignKey(UIS,on_delete=models.CASCADE)
    familyComposition = models.ForeignKey(FamilyComposition,on_delete=models.CASCADE)
    otherSources_of_fi_desc = models.CharField(max_length = 100)
    otherSources_of_fi = models.CharField(max_length = 15)

class ListofExpenses(models.Model):
    listofExpenses =  models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    uis = models.ForeignKey(UIS,on_delete=models.CASCADE)
    house = models.CharField(max_length = 20)
    amt_house = models.CharField(max_length = 10)
    lot = models.CharField(max_length = 20)
    amt_lot = models.CharField(max_length = 10)
    ligth_source = models.CharField(max_length = 100)
    amt_ligth_source = models.CharField(max_length = 50)
    water_source = models.CharField(max_length = 100)
    amt_water_source = models.CharField(max_length=50)
    other_expenses = models.CharField(max_length = 150)
    amt_other_expenses = models.CharField(max_length = 70)
    def __str__(self):
        return f"{self.listofExpenses}"
class ProblemPresented(models.Model):
    problemPresented = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    uis = models.ForeignKey(UIS,on_delete=models.CASCADE)
    problem = models.CharField(max_length = 250)
    prob_desc = models.CharField(max_length = 250)
    def __str__(self):
        return f"{self.problemPresented}"
class SWA(models.Model):
    swa = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    uis = models.ForeignKey(UIS,on_delete=models.CASCADE)
    swa_desc = models.CharField(max_length = 1500)
    def __str__(self):
        return f"{self.swa}"
class Recommendations(models.Model):
    recommendation = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    uis = models.ForeignKey(UIS,on_delete=models.CASCADE)
    type_of_assistance = models.CharField(max_length = 50)
    amt_of_assistance = models.CharField(max_length = 25)
    mode_of_assistance = models.CharField(max_length = 25)
    fund_source = models.CharField(max_length = 15)
    def __str__(self):
        return f"{self.recommendation}"
class SCSR(models.Model):
    scsr = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    uis = models.ForeignKey(UIS,on_delete=models.CASCADE)
    employer = models.CharField(max_length = 150)
    special_skill = models.CharField(max_length = 50)
    date_admission = models.CharField(max_length = 30)
    room = models.CharField(max_length = 30)
    tdd = models.CharField(max_length = 50)
    housing_material = models.CharField(max_length = 100)
    fuel_source = models.CharField(max_length = 100)
    problem_presented = models.CharField(max_length = 300)
class MSSAT(models.Model):
    mssat = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    uis = models.ForeignKey(UIS,on_delete=models.CASCADE)
    doac = models.CharField(max_length = 50)#date of admited/consulted
    venue = models.CharField(max_length = 50,default="")
    category = models.CharField(max_length = 20,default="")
    basic_ward = models.CharField(max_length = 50,default='NONE')
    non_basic = models.CharField(max_length = 50,default='NONE')
    mss_no = models.CharField(max_length = 50)
    tla = models.CharField(max_length = 50)#TYLE OF LIVING ARRANGEMENT
    src_referal_name = models.CharField(max_length = 50)
    address = models.CharField(max_length = 150)
    cnum = models.CharField(max_length = 20)
    employer = models.CharField(max_length = 100,default="NONE")
    phil_mem = models.CharField(max_length = 20)
    mswd_cassif = models.CharField(max_length = 30)
    marginalized_sec_mem = models.CharField(max_length = 50)
    fuel_source = models.CharField(max_length = 100)
    amt_fuel_source = models.CharField(max_length = 30,default=[0,0,0,0])
    clothing_amt = models.CharField(max_length = 10)
    duration_of_prob = models.CharField(max_length = 100)
    prev_treatment = models.CharField(max_length = 100)
    health_accessibility_prob = models.CharField(max_length = 100)