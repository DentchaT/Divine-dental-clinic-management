from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LoginView 
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('login_user',LoginView.as_view(template_name='login.html')),
    path('logout/', views.logout_view, name='logout'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    #------------------------------------------------------------------------------------
    #-----------------------------FOR DOCTOR---------------------------------------------
    #------------------------------------------------------------------------------------
    path('dashboard/', views.dashboard, name='dashboard'),
    path('queue/', views.queue, name='queue'),
    path('appointments/', views.appointments, name='appointments'),
    path('edit_appointment/<int:pk>', views.edit_appointment, name='edit_appointment'),  
    path('queue_appointment/<int:pk>', views.queue_appointment, name='queue_appointment'),
    path('delete_appointments/<pk>', views.delete_appointments, name='delete_appointments'),
    path('patient_treatment/', views.patient_treatment, name='patient_treatment'),
    path('online_diary/', views.online_diary, name='online_diary'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('patient_card/<pk>', views.patient_card, name='patient_card'), 
    path('queue_schedule_appointment/<int:pk>', views.queue_schedule_appointment, name='queue_schedule_appointment'),
    path('treatment_statement/<pk>', views.treatment_statement, name='treatment_statement'),
    path('individual_statement/<pk>', views.individual_statement, name='individual_statement'),
    path('leave_application/', views.leave_application, name='leave_application'),
    path('download_bill/<pk>',views.download_bill,name='download_bill'),
    path('download_prescription/<pk>',views.download_prescription,name='download_prescription'),
    path('download_labrequest/<pk>',views.download_labrequest,name='download_labrequest'),
    path('download_xrayrequest/<pk>',views.download_xrayrequest,name='download_xrayrequest'),
    path('download_referralnote/<pk>',views.download_referralnote,name='download_referralnote'),
    path('download_sickleave/<pk>',views.download_sickleave,name='download_sickleave'),
    path('download_history/<pk>',views.download_history,name='download_history'), 
    #------------------------------------------------------------------------------------
    #-----------------------------FOR ADMIN----------------------------------------------
    #------------------------------------------------------------------------------------
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_actions/', views.admin, name='admin_actions'),
    path('admin_queue/', views.admin_queue, name='admin_queue'),
    path('admin_appointments/', views.admin_appointments, name='admin_appointments'),
    path('admin_edit_appointment/<int:pk>', views.admin_edit_appointment, name='admin_edit_appointment'), 
    path('admin_queue_appointment/<int:pk>', views.admin_queue_appointment, name='admin_queue_appointment'),
    path('admin_delete_appointments/<pk>', views.admin_delete_appointments, name='admin_delete_appointments'),
    path('admin_patient_treatment/', views.admin_patient_treatment, name='admin_patient_treatment'),
    path('admin_online_diary/', views.admin_online_diary, name='admin_online_diary'),
    path('admin_my_profile/', views.admin_my_profile, name='admin_my_profile'),
    path('admin_patient_card/<pk>', views.admin_patient_card, name='admin_patient_card'),
    path('admin_queue_schedule_appointment/<int:pk>', views.admin_queue_schedule_appointment, name='admin_queue_schedule_appointment'),
    path('admin_treatment_statement/<pk>', views.admin_treatment_statement, name='admin_treatment_statement'),
    path('admin_individual_statement/<pk>', views.admin_individual_statement, name='admin_individual_statement'),
    path('admin_leave_application/', views.admin_leave_application, name='admin_leave_application'),
    path('admin_download_bill/<pk>',views.admin_download_bill,name='admin_download_bill'),
    path('admin_download_prescription/<pk>',views.admin_download_prescription,name='admin_download_prescription'),
    path('admin_download_labrequest/<pk>',views.admin_download_labrequest,name='admin_download_labrequest'),
    path('admin_download_xrayrequest/<pk>',views.admin_download_xrayrequest,name='admin_download_xrayrequest'),
    path('admin_download_referralnote/<pk>',views.admin_download_referralnote,name='admin_download_referralnote'),
    path('admin_download_sickleave/<pk>',views.admin_download_sickleave,name='admin_download_sickleave'),
    path('admin_download_history/<pk>',views.admin_download_history,name='admin_download_history'),

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)