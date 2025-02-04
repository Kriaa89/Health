from django.contrib import admin
from .models import Nurse

# Register your models here.

@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'license_number', 'is_available', 'average_rating')
    list_filter = ('specialization', 'is_available')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'license_number')
    readonly_fields = ('average_rating', 'total_reviews')
