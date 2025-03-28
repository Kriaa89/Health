from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'time', 'type', 'status')
    list_filter = ('status', 'type', 'date', 'doctor', 'patient')
    search_fields = ('doctor__first_name', 'doctor__last_name', 
                    'patient__first_name', 'patient__last_name',
                    'reason', 'notes', 'symptoms', 'diagnosis')
    date_hierarchy = 'date'
    ordering = ('-date', '-time')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('doctor', 'patient', 'date', 'time', 'type', 'status')
        }),
        ('Appointment Details', {
            'fields': ('reason', 'symptoms', 'home_address')
        }),
        ('Medical Information', {
            'classes': ('collapse',),
            'fields': ('diagnosis', 'prescription', 'notes')
        }),
        ('System Information', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
