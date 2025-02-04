from django.contrib import admin
from .models import Patient, Appointment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'emergency_contact_name')
    search_fields = ('user__username', 'emergency_contact_name')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('patient__user__username', 'doctor__user__username', 'symptoms')
