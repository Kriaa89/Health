from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]
    ROLE_CHOICES = [
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('PATIENT', 'Patient'),
    ]
    
    # Override groups and user_permissions with custom related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    role = models.CharField(max_length=7, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
