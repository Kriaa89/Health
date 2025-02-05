from django.contrib import admin
from .models import Patient, MalePatient, FemalePatient, Appointment, Review

class MalePatientInline(admin.StackedInline):
    model = MalePatient
    can_delete = False

class FemalePatientInline(admin.StackedInline):
    model = FemalePatient
    can_delete = False

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'emergency_contact_name')
    list_filter = ('blood_type', 'user__gender')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'emergency_contact_name')
    
    def get_inlines(self, request, obj=None):
        if obj and obj.user.gender == 'MALE':
            return [MalePatientInline]
        elif obj and obj.user.gender == 'FEMALE':
            return [FemalePatientInline]
        return []

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'type', 'status')
    list_filter = ('status', 'type', 'date')
    search_fields = ('patient__user__username', 'doctor__user__username', 'symptoms', 'diagnosis')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'nurse', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('patient__user__username', 'doctor__user__username', 'nurse__user__username', 'comment')
    readonly_fields = ('created_at',)
