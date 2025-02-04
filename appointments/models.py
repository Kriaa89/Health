from django.db import models
from patients.models import Patient
from doctors.models import Doctor

# Create your models here.

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    date = models.DateField()
    time = models.TimeField()
    symptoms = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        ordering = ['-date', '-time']
        # Ensure no double bookings for doctors
        unique_together = ['doctor', 'date', 'time']

    def __str__(self):
        return f"{self.patient}'s appointment with {self.doctor} on {self.date}"
