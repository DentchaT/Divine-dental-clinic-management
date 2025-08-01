from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#-----------ADMIN MODEL--------------
class Admin(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=50)
    def __str__(self):
        return f"{self.name}"

#-----------DOCTOR MODEL--------------
class Doctor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=50)
    def __str__(self):
        return f"{self.name}"
    
#----------------------PATIENT MODEL------------------------
class Patient(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=50)
    residence=models.CharField(max_length=100, null=True,blank=True)
    gender=models.CharField(max_length=100, null=True,blank=True)
    #----patient_details-----------
    date_of_birth=models.DateField(null=True,blank=True)
    email=models.EmailField(unique=True,null=True,blank=True)       

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

#------------------------QUEUE--------------------------------
class Queue(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    type = models.CharField(max_length=150, null=True,blank=True)#-------for CASH or INSURANCE-----------
    number = models.CharField(max_length=150)
    id_number = models.CharField(max_length=150)
    date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    doctor = models.CharField(max_length=150, null=True,blank=True)
    procedure = models.CharField(max_length=150, null=True,blank=True)
    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name}  queued for Dr.{self.doctor} on {self.date} "

#-------------------APPOINTMENTS----------------------------------
class Appointment(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    date = models.DateField()
    doctor = models.CharField(max_length=150, null=True,blank=True)
    procedure = models.CharField(max_length=150, null=True,blank=True)
    room = models.CharField(max_length=150, null=True,blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return f"{self.patient.first_name}'s appointment with Dr. {self.doctor} on {self.date} an {self.start_time}"
    
#-------------------PATIENT HISTORY----------------------------------
class PatientHistory(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor = models.CharField(max_length=150, null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    Hp_CO = models.CharField(max_length=1500, null=True,blank=True)
    PM_Hx = models.CharField(max_length=1500, null=True,blank=True)
    PD_Hx = models.CharField(max_length=1500, null=True,blank=True)
    Soft_Tissue = models.CharField(max_length=1500, null=True,blank=True)
    Hard_Tissue_General = models.CharField(max_length=1500, null=True,blank=True)
    Hard_Tissue_Decayed = models.CharField(max_length=1500, null=True,blank=True)
    Hard_Tissue_Filled = models.CharField(max_length=1500, null=True,blank=True)
    Hard_Tissue_Missing = models.CharField(max_length=1500, null=True,blank=True)
    Hard_Tissue_Other = models.CharField(max_length=1500, null=True,blank=True)
    Investigations = models.CharField(max_length=1500, null=True,blank=True)
    Occlusal_Exam = models.CharField(max_length=1500, null=True,blank=True)
    Findings = models.CharField(max_length=1500, null=True,blank=True)
    Plan = models.CharField(max_length=1500, null=True,blank=True)
    Rx_Done = models.CharField(max_length=1500, null=True,blank=True)
    TCA = models.CharField(max_length=1500, null=True,blank=True)
    def __str__(self):
        return f"{self.patient}'s history by {self.doctor} on {self.created_at}"
    
#-------------------LEAVE----------------------------------
class LeaveApplication(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    type = models.CharField(max_length=500, null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    def __str__(self):
        return f"{self.type} leave requested by {self.user} on {self.start_date} until {self.end_date}"
    
#-------------MEDICAL CONDITION----------------------------
class MedicalCondition(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    medical_condition = models.CharField(max_length=1500, null=True, blank=True)
    drugs = models.CharField(max_length=1500,null=True, blank=True)
    allergies = models.CharField(max_length=1500,null=True, blank=True)
    pregnancy = models.CharField(max_length=1500,null=True, blank=True) 
    def __str__(self):
        return f"{self.patient}'s Medical conditions "

#-------------VITALS---------------------------------------
class Vitals(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    systolic = models.CharField(max_length=1500, null=True, blank=True)
    diastolic = models.CharField(max_length=1500,null=True, blank=True)
    weight = models.CharField(max_length=1500,null=True, blank=True)
    height = models.CharField(max_length=1500,null=True, blank=True)
    hip = models.CharField(max_length=1500,null=True, blank=True)
    waist = models.CharField(max_length=1500,null=True, blank=True)
    temp = models.CharField(max_length=1500,null=True, blank=True)
    pulse = models.CharField(max_length=1500,null=True, blank=True)
    respiration = models.CharField(max_length=1500,null=True, blank=True)
    oxygen_saturation = models.CharField(max_length=1500,null=True, blank=True)
    pain = models.CharField(max_length=1500,null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.patient}'s vitals created on {self.created_at}"
    
#------------PRESCRIPTION--------------------------------------
class Prescription(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    prescription = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.patient}'s prescription created on {self.created_at}"
    
#------------LAB REQUEST--------------------------------------
class LabRequest(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    lab_request = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.patient}'s Lab request created on {self.created_at}"
    
#------------XRAY REQUEST--------------------------------------
class XrayRequest(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    xray_request = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.patient}'s xray request created on {self.created_at}"
    
#------------REFERRAL NOT--------------------------------------
class ReferralNote(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    referral_note = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.patient}'s referral note  created on {self.created_at}"
    
#------------SICK LEAVE--------------------------------------
class SickLeave(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    sick_leave = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.patient}'s sick leave  created on {self.created_at}"
    
#---------------UPLOADS--------------------------------------
class uploads(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    type = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    xray = models.ImageField(upload_to='img/xrays')
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} xray for {self.patient} on {self.created_at}"
    
#---------------BILLING--------------------------------------
class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service1 = models.CharField(max_length=150, null=True, blank=True)
    service2 = models.CharField(max_length=150, null=True, blank=True)
    service3 = models.CharField(max_length=150, null=True, blank=True)
    unit1 = models.CharField(max_length=150, null=True, blank=True)
    unit2 = models.CharField(max_length=150, null=True, blank=True)
    unit3 = models.CharField(max_length=150, null=True, blank=True)
    cost1 = models.CharField(max_length=150, null=True, blank=True)
    cost2 = models.CharField(max_length=150, null=True, blank=True)
    cost3 = models.CharField(max_length=150, null=True, blank=True)
    waiver_reason = models.CharField(max_length=150, null=True, blank=True)
    waiver = models.CharField(max_length=150, null=True, blank=True)
    lab = models.CharField(max_length=150, null=True, blank=True)
    deduct = models.CharField(max_length=150, null=True, blank=True)
    total = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"Shs.{self.total} bill for {self.patient} on {self.created_at}"
