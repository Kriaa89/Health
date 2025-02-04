from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    office_hours = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Dr. {self.user.username}"
