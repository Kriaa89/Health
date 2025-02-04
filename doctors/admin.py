from django.contrib import admin
from .models import Doctor

# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'license_number', 'consultation_fee', 'is_available', 'average_rating')
    list_filter = ('specialty', 'is_available')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialty', 'license_number')
    readonly_fields = ('average_rating', 'total_reviews')
