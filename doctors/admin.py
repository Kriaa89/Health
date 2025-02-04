from django.contrib import admin
from .models import Doctor

# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'office_hours')
    search_fields = ('user__username', 'specialization')
