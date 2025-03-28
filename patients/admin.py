from django.contrib import admin
from .models import Patient, Review
from django.utils.html import format_html

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'emergency_contact_name', 'gender_display')
    list_filter = ('blood_type', 'is_male')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'emergency_contact_name')
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'blood_type', 'is_male')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Insurance Information', {
            'fields': ('insurance_provider', 'insurance_id')
        }),
        ('Medical Information', {
            'fields': ('allergies', 'chronic_conditions', 'current_medications', 'last_checkup')
        }),
        ('Male-Specific Information', {
            'classes': ('collapse',),
            'fields': ('prostate_exam', 'cardiac_test', 'psa_level')
        }),
        ('Female-Specific Information', {
            'classes': ('collapse',),
            'fields': ('pregnant', 'last_menstrual', 'mammogram_date', 'pap_smear_date', 'gynecological_history')
        }),
    )
    
    def gender_display(self, obj):
        if obj.is_male:
            return format_html('<span style="color: blue;">Male</span>')
        return format_html('<span style="color: purple;">Female</span>')
    gender_display.short_description = 'Gender'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('patient__user__username', 'doctor__user__username', 'comment')
    readonly_fields = ('created_at',)
