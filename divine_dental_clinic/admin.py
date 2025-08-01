from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Queue)
admin.site.register(Appointment)
admin.site.register(PatientHistory)
admin.site.register(MedicalCondition)
admin.site.register(Vitals)
admin.site.register(Prescription)
admin.site.register(LabRequest)
admin.site.register(XrayRequest)
admin.site.register(ReferralNote)
admin.site.register(SickLeave)
admin.site.register(uploads)
admin.site.register(Billing)