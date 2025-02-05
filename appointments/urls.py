from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('manage/<int:appointment_id>/', views.manage_appointment, name='manage_appointment'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('doctor/schedule/', views.doctor_schedule, name='doctor_schedule'),
    path('new/', views.new_appointment, name='new_appointment'),
    path('patient/records/', views.patient_records, name='patient_records'),
]
