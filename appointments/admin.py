from django.contrib import admin
from .models import Appointment

# Register your models here.

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'doctor', 'patient')
    search_fields = ('doctor__first_name', 'doctor__last_name', 
                    'patient__first_name', 'patient__last_name',
                    'reason', 'notes')
    date_hierarchy = 'date'
    ordering = ('-date', '-time')
