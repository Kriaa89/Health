from django.db import models
from accounts.models import CustomUser

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3)
    allergies = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    symptoms = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.patient.user.username}'s appointment on {self.date}"
