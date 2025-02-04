from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('role-select/', views.role_selection, name='role_select'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('appointment/book/', views.book_appointment, name='book_appointment'),
    path('appointment/<int:appointment_id>/manage/', views.manage_appointment, name='manage_appointment'),
]
