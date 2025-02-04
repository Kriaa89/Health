from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=8)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
