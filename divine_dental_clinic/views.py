from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from .models import *
from datetime import date, timedelta

# Create your views here.

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------LOGIN AND AUTHENTICATION------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
def logout_view(request):
    auth_logout(request)
    return redirect('login')
    
#----CHECKING IF USER IS ADMIN OR DOCTOR--------------
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user): 
    return user.groups.filter(name='DOCTOR').exists()

#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN OR DOCTOR 
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')
    elif is_doctor(request.user):
        return redirect('dashboard') 
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#----------------LOGIN AND AUTHENTICATION END HERE-----------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#--------------for pdf downloadimg and printing--------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#--------------for pdf downloadimg and printing end here-----------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------


#------------------------------------------------------------------------
#------------------------------------------------------------------------
#---------------------DOCTOR VIEWS---------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
@login_required(login_url="login")
@user_passes_test(is_doctor)
def dashboard(request):
    today=date.today()
    tomorrow=today + timedelta(days=1)
    appointments = Appointment.objects.filter(date=today).order_by('-id')
    appoint = Appointment.objects.filter(date=tomorrow).order_by('-id')
    queueds=Queue.objects.filter(date=today).order_by('-id')
    mydict={
        'queueds':queueds,
        'today':today,
        'appointments':appointments,
        'tomorrow':tomorrow,
        'appoint':appoint
    }
    return render(request, 'dashboard.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def queue(request):
    today=date.today()
    queueds=Queue.objects.filter(date=today).order_by('-id')

    type_q = request.GET.get('type_q')
    number_q = request.GET.get('number_q')
    id_number_q = request.GET.get('id_number_q')
    first_name_q = request.GET.get('first_name_q')
    last_name_q = request.GET.get('last_name_q')

    if type_q and type_q.strip() != '---Select Visit Type---' and type_q.strip() != '':
        queueds = queueds.filter(type=type_q)
    if number_q:
        queueds = queueds.filter(number=number_q)
    if id_number_q:
        queueds = queueds.filter(id_number=id_number_q)
    if first_name_q:
        queueds = queueds.filter(patient__first_name__icontains=first_name_q)
    if last_name_q:
        queueds = queueds.filter(patient__last_name__icontains=last_name_q)

    mydict={
        'queueds':queueds,
        'today':today,
    }
    return render(request, 'queue.html', context=mydict)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def queue_appointment(request,pk):
    today=date.today()

    appointment = get_object_or_404(Appointment, pk=pk)
    patient_queue = appointment.patient.queue_set.latest('id')

    queue = Queue.objects.create(
        patient=appointment.patient,
        number=patient_queue.number,
        id_number=patient_queue.id_number,
        doctor=patient_queue.doctor,
        date=today,
    )
    return redirect('queue')

@login_required(login_url="login")
@user_passes_test(is_doctor)
def appointments(request):
    today = date.today()
    appointments = Appointment.objects.all().order_by('-id')

    number_q = request.GET.get('number')
    date_q = request.GET.get('date')
    first_name_q = request.GET.get('first_name')
    last_name_q = request.GET.get('last_name')

    if date_q:
        appointments = appointments.filter(date=date_q)
    if first_name_q:
        appointments = appointments.filter(patient__first_name__icontains=first_name_q)
    if last_name_q:
        appointments = appointments.filter(patient__last_name__icontains=last_name_q)
    if number_q:
        appointments = appointments.filter(patient__id=number_q)

    mydict={
        'today':today,
        'appointments':appointments
    }
    return render(request, 'appointments.html', context=mydict)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def edit_appointment(request, pk):
    appointment=get_object_or_404(Appointment,pk=pk)
    patient=appointment.patient
    doctors=Doctor.objects.all()

    mydic = {
        'patient':patient,
        'doctors':doctors
    }

    if request.method == 'POST':
        appointment.date=request.POST['date']
        appointment.doctor=request.POST['doctor']
        appointment.procedure=request.POST['procedure']
        appointment.room=request.POST['room']
        appointment.start_time=request.POST['start_time']
        appointment.end_time=request.POST['end_time']
        appointment.patient = patient
        appointment.save()
        return redirect('appointments')

    return render(request, 'schedule-appointment.html', context=mydic)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def delete_appointments(request,pk):
    appointment = get_object_or_404(Appointment,pk=pk)
    appointment.delete()
    return redirect('appointments')

@login_required(login_url="login")
@user_passes_test(is_doctor)
def patient_treatment(request):
    patients = Patient.objects.all().order_by('-id')
    first_name_q = request.GET.get('first_name')

    if first_name_q:
        patients = patients.filter(first_name__icontains=first_name_q)

    mydict = {
        'patients':patients
    }
    return render(request, 'patient-treatment.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def online_diary(request):
    appointments=Appointment.objects.all()
    mydict = {
        'appointments':appointments
    }
    return render(request, 'online-diary.html', context=mydict)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def my_profile(request):
    bio = Doctor.objects.get(user=request.user)
    leaves = LeaveApplication.objects.all().order_by('-id')
    mydict = {
        'bio':bio,
        'leaves':leaves
    }
    return render(request, 'my-profile.html', context=mydict)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def patient_card(request,pk):
    today=date.today()
    queue = get_object_or_404(Queue, pk = pk)
    patient = queue.patient
    patient_history = PatientHistory.objects.filter(patient=patient).order_by('-id')
    patient_conditions = get_object_or_404(MedicalCondition, patient=patient)
    vitals = get_object_or_404(Vitals, patient=patient) 
    prescription = Prescription.objects.filter(patient=patient).order_by('-id')
    lab_request = LabRequest.objects.filter(patient=patient).order_by('-id')
    xray_request = XrayRequest.objects.filter(patient=patient).order_by('-id')
    referral = ReferralNote.objects.filter(patient=patient).order_by('-id')
    sick_leave = SickLeave.objects.filter(patient=patient).order_by('-id')
    upload = uploads.objects.filter(patient=patient).order_by('-id')
    try:
        bill = Billing.objects.filter(patient=patient).latest('id') 
    except:
        bill = None
    mydict = {
        'queue':queue,
        'today':today,
        'patient':patient,
        'patient_history':patient_history,
        'patient_conditions':patient_conditions,
        'vitals':vitals,
        'prescription': prescription,
        'lab_request': lab_request,
        'xray_request': xray_request,
        'referral': referral,
        'sick_leave': sick_leave,
        'upload':upload,
        'bill':bill
    }
    if request.method == 'POST':
        if 'medical_condition' in request.POST:
            patient_conditions.medical_condition=request.POST['condition']
            patient_conditions.allergies=request.POST['allergies']
            patient_conditions.drugs=request.POST['drugs']
            patient_conditions.pregnancy=request.POST['pregnancy']
            patient_conditions.save()
            return redirect('patient_card',pk=queue.id)
        elif 'vitals' in request.POST:
            vitals.systolic=request.POST['systolic']
            vitals.diastolic=request.POST['diastolic']
            vitals.weight=request.POST['weight']
            vitals.height=request.POST['height']
            vitals.hip=request.POST['hip']
            vitals.waist=request.POST['waist']
            vitals.temp=request.POST['temp']
            vitals.pulse=request.POST['pulse']
            vitals.respiration=request.POST['respiration']
            vitals.oxygen_saturation=request.POST['oxygen_saturation']
            vitals.pain=request.POST['pain']
            vitals.save()
            return redirect('patient_card',pk=queue.id)
        elif 'prescription' in request.POST:
            prescription = Prescription.objects.create(
                patient=patient,
                prescription=request.POST.get('prescribe'),
            )
            return redirect('patient_card',pk=queue.id)
        elif 'lab_request' in request.POST:
            lab_request = LabRequest.objects.create(
                patient=patient,
                lab_request=request.POST.get('lab'),
            )
            return redirect('patient_card',pk=queue.id)
        elif 'xray_request' in request.POST:
            xray_request = XrayRequest.objects.create(
                patient=patient,
                xray_request=request.POST.get('xray'),
            )
            return redirect('patient_card',pk=queue.id)
        elif 'referral_note' in request.POST:
            referral = ReferralNote.objects.create(
                patient=patient,
                referral_note=request.POST.get('referral'),
            )
            return redirect('patient_card',pk=queue.id)  
        elif 'sick_leave' in request.POST:
            sick_leave = SickLeave.objects.create(
                patient=patient,
                sick_leave=request.POST.get('leave'),
            )
            return redirect('patient_card',pk=queue.id)  
        elif 'upload' in request.POST:
            upload = uploads.objects.create(
                patient=patient,
                type=request.POST.get('type'),
                name=request.POST.get('name'),
                xray=request.FILES.get('xray'),
            )
            return redirect('patient_card',pk=queue.id)
        elif 'bill' in request.POST:
            bill = Billing.objects.create(
                patient=patient,
                service1=request.POST.get('service1'),
                service2=request.POST.get('service2'),
                service3=request.POST.get('service3'),
                unit1=request.POST.get('unit1'),
                unit2=request.POST.get('unit2'),
                unit3=request.POST.get('unit3'),
                cost1=request.POST.get('cost1'),
                cost2=request.POST.get('cost2'),
                cost3=request.POST.get('cost3'),
                waiver_reason=request.POST.get('waiver-reason'),
                waiver=request.POST.get('waiver'),
                lab=request.POST.get('lab'),
                deduct=request.POST.get('deduct'),
                total=request.POST.get('total'),
            )
            return redirect('patient_card',pk=queue.id)
    return render(request, 'patient-card.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def queue_schedule_appointment(request,pk):
    doctors=Doctor.objects.all()
    queue = get_object_or_404(Queue,pk=pk)
    patient = queue.patient

    mydic = {
        'patient':patient,
        'doctors':doctors,
    }

    if request.method == 'POST':
        appointment = Appointment.objects.create(
            date=request.POST['date'],
            doctor=request.POST['doctor'],
            procedure=request.POST['procedure'],
            room=request.POST['room'],
            start_time=request.POST['start_time'],
            end_time=request.POST['end_time'],
            patient = patient
        )
        return redirect('appointments')
    return render(request, 'queue-schedule-appointment_two.html', context=mydic) 

@login_required(login_url="login")
@user_passes_test(is_doctor)
def treatment_statement(request,pk):
    today = date.today()
    patient = get_object_or_404(Patient,pk=pk)
    historys = PatientHistory.objects.filter(patient=patient).order_by('-id').exclude(created_at=today)
    patient_history, created = PatientHistory.objects.get_or_create(patient=patient,created_at=today)
    mydic = {
        'patient':patient,
        'historys':historys,
        'patient_history':patient_history
    }
    if request.method == 'POST':
        patient_history.doctor = request.user.doctor.name
        patient_history.Hp_CO = request.POST['HPC']
        patient_history.PM_Hx = request.POST['PM']
        patient_history.PD_Hx = request.POST['PD']
        patient_history.Soft_Tissue = request.POST['ST']
        patient_history.Hard_Tissue_General = request.POST['G']
        patient_history.Hard_Tissue_Decayed = request.POST['D']
        patient_history.Hard_Tissue_Filled = request.POST['F']
        patient_history.Hard_Tissue_Missing = request.POST['M']
        patient_history.Hard_Tissue_Other = request.POST['O']
        patient_history.Investigations = request.POST['I']
        patient_history.Occlusal_Exam = request.POST['OE']
        patient_history.Findings = request.POST['F']
        patient_history.Plan = request.POST['PD']
        patient_history.Rx_Done = request.POST['RD']
        patient_history.TCA = request.POST['TCA']
        patient_history.save()
        return redirect('treatment_statement', pk=patient.id)
    return render(request, 'treatment-statement.html',context=mydic)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def individual_statement(request,pk):
    patient=get_object_or_404(Patient,pk=pk)
    bill = Billing.objects.filter(patient=patient).order_by('-id') 
    mydict={
        'bill':bill,
        'patient':patient
    }
    return render(request, 'individual-statement.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def leave_application(request):
    if request.method == 'POST':
        leave = LeaveApplication.objects.create(
            user = request.user,
            type = request.POST['type'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date']
        )
        return redirect('my_profile')
    return render(request, 'leave-application.html')

@login_required(login_url="login")
@user_passes_test(is_doctor)
def download_bill(request,pk):
    today=date.today()
    patient=get_object_or_404(Patient,pk=pk) 
    history=PatientHistory.objects.filter(patient=patient).latest('id')
    bill=Billing.objects.filter(patient=patient).latest('id')
    mydict={
        'history':history,
        'today':today,
        'bill': bill,
        'patient': patient
    }
    return render_to_pdf('download_bill.html',mydict) 

@login_required(login_url="login")
@user_passes_test(is_doctor)
def download_prescription(request,pk): 
    today=date.today()
    patient=get_object_or_404(Patient,pk=pk) 
    history=PatientHistory.objects.filter(patient=patient).latest('id')
    bill=Billing.objects.filter(patient=patient).latest('id')
    prescribe=Prescription.objects.filter(patient=patient).latest('id')
    mydict={
        'prescribe':prescribe,
        'history':history,
        'today':today,
        'bill': bill,
        'patient': patient
    }
    return render_to_pdf('download_prescription.html',mydict)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def download_labrequest(request,pk):
    today=date.today()
    patient=get_object_or_404(Patient,pk=pk) 
    history=PatientHistory.objects.filter(patient=patient).latest('id')
    bill=Billing.objects.filter(patient=patient).latest('id')
    labrequest=LabRequest.objects.filter(patient=patient).latest('id')
    mydict={
        'labrequest':labrequest,
        'history':history,
        'today':today,
        'bill': bill,
        'patient': patient
    }
    return render_to_pdf('download_labrequest.html',mydict)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def download_xrayrequest(request,pk):
    today=date.today()
    patient=get_object_or_404(Patient,pk=pk) 
    history=PatientHistory.objects.filter(patient=patient).latest('id')
    bill=Billing.objects.filter(patient=patient).latest('id')
    xrayrequest=XrayRequest.objects.filter(patient=patient).latest('id')
    mydict={
        'xrayrequest':xrayrequest,
        'history':history,
        'today':today,
        'bill': bill,
        'patient': patient
    }
    return render_to_pdf('download_xrayrequest.html',mydict)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def download_referralnote(request,pk):
    today=date.today()
    patient=get_object_or_404(Patient,pk=pk) 
    history=PatientHistory.objects.filter(patient=patient).latest('id')
    bill=Billing.objects.filter(patient=patient).latest('id')
    referralnote=ReferralNote.objects.filter(patient=patient).latest('id')
    mydict={
        'referralnote':referralnote,
        'history':history,
        'today':today,
        'bill': bill,
        'patient': patient
    }
    return render_to_pdf('download_referralnote.html',mydict)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def download_sickleave(request,pk):
    today=date.today()
    patient=get_object_or_404(Patient,pk=pk) 
    history=PatientHistory.objects.filter(patient=patient).latest('id')
    bill=Billing.objects.filter(patient=patient).latest('id')
    sickleave=SickLeave.objects.filter(patient=patient).latest('id')
    mydict={
        'sickleave':sickleave,
        'history':history,
        'today':today,
        'bill': bill,
        'patient': patient
    }
    return render_to_pdf('download_sickleave.html',mydict)

@login_required(login_url="login")
@user_passes_test(is_doctor)
def download_history(request,pk):
    history = get_object_or_404(PatientHistory,pk=pk)
    patient = history.patient 
    today = date.today()
    mydict = {
        'today': today,
        'history': history,
        'patient': patient
    }
    return render_to_pdf('download_history.html',mydict)
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#-------------DOCTOR VIEWS END HERE--------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------




#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------ADMIN VIEWS-------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_dashboard(request):
    today=date.today()
    tomorrow=today + timedelta(days=1)
    appointments = Appointment.objects.filter(date=today).order_by('-id')
    appoint = Appointment.objects.filter(date=tomorrow).order_by('-id')
    queueds=Queue.objects.filter(date=today).order_by('-id')
    mydict={
        'queueds':queueds,
        'today':today,
        'appointments':appointments,
        'tomorrow':tomorrow,
        'appoint':appoint
    }
    return render(request, 'admin-dashboard.html', context=mydict)

#@login_required(login_url="login")
#@user_passes_test(is_admin)
def admin(request):
    DoctorUserForm = Add_Doctor_UserForm()
    DoctorForm = Add_Doctor_Form()
    AdminUserForm = Add_Admin_UserForm()
    AdminForm = Add_Admin_Form()
    doctors=Doctor.objects.all()
    QueueForm=Queue_Patient_Form()
    PatientForm=Add_Patient_Form()

    mydict ={
        'DoctorUserForm':DoctorUserForm,
        'DoctorForm':DoctorForm,
        'AdminUserForm':AdminUserForm,
        'AdminForm':AdminForm,
        'doctors':doctors,
        'QueueForm':QueueForm,
        'PatientForm':PatientForm,
    }

    if request.method == 'POST':

        if 'add_doctor' in request.POST:
            DoctorUserForm = Add_Doctor_UserForm(request.POST)
            DoctorForm = Add_Doctor_Form(request.POST)
            if DoctorUserForm.is_valid() and DoctorForm.is_valid():
                user = DoctorUserForm.save()
                user.set_password(user.password)
                user.save()
                doctor=DoctorForm.save(commit=False)
                doctor.user = user
                doctor = doctor.save()
                my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
                my_doctor_group[0].user_set.add(user)
            return redirect('admin_actions')
        
        elif 'add_admin' in request.POST:
            AdminUserForm = Add_Admin_UserForm(request.POST)
            AdminForm = Add_Admin_Form(request.POST)
            if AdminUserForm.is_valid() and AdminForm.is_valid():
                user = AdminUserForm.save()
                user.set_password(user.password)
                user.save()
                admin=AdminForm.save(commit=False)
                admin.user = user
                admin = admin.save()
                my_admin_group = Group.objects.get_or_create(name='ADMIN')
                my_admin_group[0].user_set.add(user)
            return redirect('admin_actions')
        
        elif 'queue_patient' in request.POST:
            QueueForm=Queue_Patient_Form(request.POST)
            PatientForm=Add_Patient_Form(request.POST)
            if QueueForm.is_valid() and PatientForm.is_valid():
                patient=PatientForm.save()
                queue=QueueForm.save(commit=False)
                queue.patient=patient
                queue.doctor=request.POST['doctor']
                queue.type=request.POST['type']
                queue.procedure=request.POST['procedure']
                queue.save()
                MedicalCondition.objects.create(patient=patient)
                Vitals.objects.create(patient=patient)
            return redirect('admin_actions')
    return render(request, 'admin.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_queue(request):
    today = date.today()
    queueds = Queue.objects.filter(date=today).order_by('-id')

    type_q = request.GET.get('type_q')
    number_q = request.GET.get('number_q')
    id_number_q = request.GET.get('id_number_q')
    first_name_q = request.GET.get('first_name_q')
    last_name_q = request.GET.get('last_name_q')

    if type_q and type_q.strip() != '---Select Visit Type---' and type_q.strip() != '':
        queueds = queueds.filter(type=type_q)
    if number_q:
        queueds = queueds.filter(number=number_q)
    if id_number_q:
        queueds = queueds.filter(id_number=id_number_q)
    if first_name_q:
        queueds = queueds.filter(patient__first_name__icontains=first_name_q)
    if last_name_q:
        queueds = queueds.filter(patient__last_name__icontains=last_name_q)

    mydict = {
        'queueds': queueds,
        'today': today,
    }
    return render(request, 'admin-queue.html', context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_queue_appointment(request,pk):
    today=date.today()

    appointment = get_object_or_404(Appointment, pk=pk)
    patient_queue = appointment.patient.queue_set.latest('id')

    queue = Queue.objects.create(
        patient=appointment.patient,
        number=patient_queue.number,
        id_number=patient_queue.id_number,
        doctor=patient_queue.doctor,
        date=today,
    )
    return redirect('admin_queue')

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_appointments(request):
    today = date.today()
    appointments = Appointment.objects.all().order_by('-id')

    number_q = request.GET.get('number')
    date_q = request.GET.get('date')
    first_name_q = request.GET.get('first_name')
    last_name_q = request.GET.get('last_name')

    if date_q:
        appointments = appointments.filter(date=date_q)
    if first_name_q:
        appointments = appointments.filter(patient__first_name=first_name_q)
    if last_name_q:
        appointments = appointments.filter(patient__last_name=last_name_q)
    if number_q:
        appointments = appointments.filter(patient_id=number_q)

    mydict={
        'today':today,
        'appointments':appointments
    }
    return render(request, 'admin-appointments.html', context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_delete_appointments(request,pk):
    appointment = get_object_or_404(Appointment,pk=pk)
    appointment.delete()
    return redirect('admin_appointments')

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_patient_treatment(request):
    patients = Patient.objects.all().order_by('-id')
    first_name_q = request.GET.get('first_name')

    if first_name_q:
        patients = patients.filter(first_name__icontains=first_name_q)

    mydict = {
        'patients':patients
    }
    return render(request, 'admin-patient-treatment.html', context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_online_diary(request):
    appointments=Appointment.objects.all()
    mydict = {
        'appointments':appointments
    }
    return render(request, 'admin-online-diary.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_my_profile(request):
    bio = Admin.objects.get(user=request.user)
    leaves = LeaveApplication.objects.all().order_by('-id')
    mydict = {
        'bio':bio,
        'leaves':leaves
    }
    return render(request, 'admin-my-profile.html', context=mydict) 

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_patient_card(request, pk):
    today=date.today()
    queue = get_object_or_404(Queue, pk = pk)
    patient = queue.patient
    patient_history = PatientHistory.objects.filter(patient=patient).order_by('-id')
    patient_conditions = get_object_or_404(MedicalCondition, patient=patient)
    vitals = get_object_or_404(Vitals, patient=patient) 
    prescription = Prescription.objects.filter(patient=patient).order_by('-id')
    lab_request = LabRequest.objects.filter(patient=patient).order_by('-id')
    xray_request = XrayRequest.objects.filter(patient=patient).order_by('-id')
    refferal = ReferralNote.objects.filter(patient=patient).order_by('-id') 
    sick_leave = SickLeave.objects.filter(patient=patient).order_by('-id')
    upload = uploads.objects.filter(patient=patient).order_by('-id')
    try:
        bill = Billing.objects.filter(patient=patient).latest('id')  
    except:
        bill = None
    mydict = {
        'queue':queue,
        'today':today,
        'patient':patient,
        'patient_history':patient_history,
        'patient_conditions':patient_conditions,
        'vitals':vitals,
        'prescription': prescription,
        'lab_request': lab_request,
        'xray_request': xray_request,
        'refferal': refferal,
        'sick_leave':sick_leave,
        'upload':upload,
        'bill': bill 
    }
    if request.method == 'POST':
        if 'medical_condition' in request.POST:
            patient_conditions.medical_condition=request.POST['condition']
            patient_conditions.allergies=request.POST['allergies']
            patient_conditions.drugs=request.POST['drugs']
            patient_conditions.pregnancy=request.POST['pregnancy']
            patient_conditions.save()
            return redirect('admin_patient_card',pk=queue.id)
        elif 'vitals' in request.POST:
            vitals.systolic=request.POST['systolic']
            vitals.diastolic=request.POST['diastolic']
            vitals.weight=request.POST['weight']
            vitals.height=request.POST['height']
            vitals.hip=request.POST['hip']
            vitals.waist=request.POST['waist']
            vitals.temp=request.POST['temp']
            vitals.pulse=request.POST['pulse']
            vitals.respiration=request.POST['respiration']
            vitals.oxygen_saturation=request.POST['oxygen_saturation']
            vitals.pain=request.POST['pain']
            vitals.save()
            return redirect('admin_patient_card',pk=queue.id)
        elif 'prescription' in request.POST:
            prescription = Prescription.objects.create(
                patient=patient,
                prescription=request.POST.get('prescribe'),
            )
            return redirect('admin_patient_card',pk=queue.id)
        elif 'lab_request' in request.POST:
            lab_request = LabRequest.objects.create(
                patient=patient,
                lab_request=request.POST.get('lab'),
            )
            return redirect('admin_patient_card',pk=queue.id)
        elif 'xray_request' in request.POST:
            xray_request = XrayRequest.objects.create(
                patient=patient,
                xray_request=request.POST.get('xray'),
            )
            return redirect('admin_patient_card',pk=queue.id)
        elif 'referral_note' in request.POST:
            referral = ReferralNote.objects.create(
                patient=patient,
                referral_note=request.POST.get('referral'),
            )
            return redirect('admin_patient_card',pk=queue.id)
        elif 'sick_leave' in request.POST:
            sick_leave = SickLeave.objects.create(
                patient=patient,
                sick_leave=request.POST.get('leave'),
            )
            return redirect('admin_patient_card',pk=queue.id)
        elif 'upload' in request.POST:
            upload = uploads.objects.create(
                patient=patient,
                type=request.POST.get('type'),
                name=request.POST.get('name'),
                xray=request.FILES.get('xray'),
            )
            return redirect('admin_patient_card',pk=queue.id)
        elif 'bill' in request.POST:
            bill = Billing.objects.create(
                patient=patient,
                service1=request.POST.get('service1'),
                service2=request.POST.get('service2'),
                service3=request.POST.get('service3'),
                unit1=request.POST.get('unit1'),
                unit2=request.POST.get('unit2'),
                unit3=request.POST.get('unit3'),
                cost1=request.POST.get('cost1'),
                cost2=request.POST.get('cost2'),
                cost3=request.POST.get('cost3'),
                waiver_reason=request.POST.get('waiver-reason'),
                waiver=request.POST.get('waiver'),
                lab=request.POST.get('lab'),
                deduct=request.POST.get('deduct'),
                total=request.POST.get('total'),
            )
            return redirect('admin_patient_card',pk=queue.id)
    return render(request, 'admin-patient-card.html', context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_queue_schedule_appointment(request, pk):
    doctors=Doctor.objects.all()
    queue = get_object_or_404(Queue,pk=pk)
    patient = queue.patient
    mydic = {
        'patient':patient,
        'doctors':doctors
    }

    if request.method == 'POST':
        appointment = Appointment.objects.create(
            date=request.POST['date'],
            doctor=request.POST['doctor'],
            procedure=request.POST['procedure'],
            room=request.POST['room'],
            start_time=request.POST['start_time'],
            end_time=request.POST['end_time'],
            patient = patient
        )
        return redirect('admin_appointments')

    return render(request, 'queue-schedule-appointment.html', context=mydic)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_edit_appointment(request, pk):
    appointment=get_object_or_404(Appointment,pk=pk)
    patient=appointment.patient
    doctors=Doctor.objects.all()

    mydic = {
        'patient':patient,
        'doctors':doctors
    }

    if request.method == 'POST':
        appointment.date=request.POST['date']
        appointment.doctor=request.POST['doctor']
        appointment.procedure=request.POST['procedure']
        appointment.room=request.POST['room']
        appointment.start_time=request.POST['start_time']
        appointment.end_time=request.POST['end_time']
        appointment.patient = patient
        appointment.save()
        return redirect('admin_appointments')

    return render(request, 'schedule-appointment_two.html', context=mydic)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_treatment_statement(request,pk):
    today = date.today()
    patient = get_object_or_404(Patient,pk=pk)
    historys = PatientHistory.objects.filter(patient=patient).order_by('-id').exclude(created_at=today)
    patient_history, created = PatientHistory.objects.get_or_create(patient=patient,created_at=today)
    mydic = {
        'patient':patient,
        'historys':historys,
        'patient_history':patient_history
    }
    if request.method == 'POST':
        patient_history.doctor = request.user.admin.name
        patient_history.Hp_CO = request.POST['HPC']
        patient_history.PM_Hx = request.POST['PM']
        patient_history.PD_Hx = request.POST['PD']
        patient_history.Soft_Tissue = request.POST['ST']
        patient_history.Hard_Tissue_General = request.POST['G']
        patient_history.Hard_Tissue_Decayed = request.POST['D']
        patient_history.Hard_Tissue_Filled = request.POST['F']
        patient_history.Hard_Tissue_Missing = request.POST['M']
        patient_history.Hard_Tissue_Other = request.POST['O']
        patient_history.Investigations = request.POST['I']
        patient_history.Occlusal_Exam = request.POST['OE']
        patient_history.Findings = request.POST['F']
        patient_history.Plan = request.POST['PD']
        patient_history.Rx_Done = request.POST['RD']
        patient_history.TCA = request.POST['TCA']
        patient_history.save()
        return redirect('admin_treatment_statement', pk=patient.id)
    return render(request, 'admin-treatment-statement.html',context=mydic)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_individual_statement(request,pk):
    patient=get_object_or_404(Patient,pk=pk)
    bill = Billing.objects.filter(patient=patient).order_by('-id')
    mydict={
        'bill':bill,
        'patient':patient
    }
    return render(request, 'admin-individual-statement.html', context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_leave_application(request):
    if request.method == 'POST':
        leave = LeaveApplication.objects.create(
            user = request.user,
            type = request.POST['type'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date']
        )
        return redirect('admin_my_profile')
    return render(request, 'admin-leave-application.html')

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_download_bill(request,pk):
    today=date.today()
    patient=get_object_or_404(Patient,pk=pk) 
    history=PatientHistory.objects.filter(patient=patient).latest('id')
    bill=Billing.objects.filter(patient=patient).latest('id')
    mydict={
        'history':history,
        'today':today,
        'bill': bill,
        'patient': patient
    }
    return render_to_pdf('download_bill.html',mydict) 

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_download_prescription(request,pk):
    today=date.today()
    patient=get_object_or_404(Patient,pk=pk) 
    history=PatientHistory.objects.filter(patient=patient).latest('id')
    bill=Billing.objects.filter(patient=patient).latest('id')
    prescribe=Prescription.objects.filter(patient=patient).latest('id')
    mydict={
        'prescribe':prescribe,
        'history':history,
        'today':today,
        'bill': bill,
        'patient': patient
    }
    return render_to_pdf('download_prescription.html',mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_download_labrequest(request,pk):
    today=date.today()
    patient=get_object_or_404(Patient,pk=pk) 
    history=PatientHistory.objects.filter(patient=patient).latest('id')
    bill=Billing.objects.filter(patient=patient).latest('id')
    labrequest=LabRequest.objects.filter(patient=patient).latest('id')
    mydict={
        'labrequest':labrequest,
        'history':history,
        'today':today,
        'bill': bill,
        'patient': patient
    }
    return render_to_pdf('download_labrequest.html',mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_download_xrayrequest(request,pk):
    today=date.today()
    patient=get_object_or_404(Patient,pk=pk) 
    history=PatientHistory.objects.filter(patient=patient).latest('id')
    bill=Billing.objects.filter(patient=patient).latest('id')
    xrayrequest=XrayRequest.objects.filter(patient=patient).latest('id')
    mydict={
        'xrayrequest':xrayrequest,
        'history':history,
        'today':today,
        'bill': bill,
        'patient': patient
    }
    return render_to_pdf('download_xrayrequest.html',mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_download_referralnote(request,pk):
    today=date.today()
    patient=get_object_or_404(Patient,pk=pk) 
    history=PatientHistory.objects.filter(patient=patient).latest('id')
    bill=Billing.objects.filter(patient=patient).latest('id')
    referralnote=ReferralNote.objects.filter(patient=patient).latest('id')
    mydict={
        'referralnote':referralnote,
        'history':history,
        'today':today,
        'bill': bill,
        'patient': patient
    }
    return render_to_pdf('download_referralnote.html',mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_download_sickleave(request,pk):
    today=date.today()
    patient=get_object_or_404(Patient,pk=pk) 
    history=PatientHistory.objects.filter(patient=patient).latest('id')
    bill=Billing.objects.filter(patient=patient).latest('id')
    sickleave=SickLeave.objects.filter(patient=patient).latest('id')
    mydict={
        'sickleave':sickleave,
        'history':history,
        'today':today,
        'bill': bill,
        'patient': patient
    }
    return render_to_pdf('download_sickleave.html',mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_download_history(request,pk):
    history = get_object_or_404(PatientHistory,pk=pk)
    patient = history.patient 
    today = date.today()
    mydict = {
        'today': today,
        'history': history,
        'patient': patient
    }
    return render_to_pdf('download_history.html',mydict)
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------ADMIN VIEWS END HERE----------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
