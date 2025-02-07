from django.db import models
from django.conf import settings

# Create your models here.

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('TIME_PROPOSED', 'Time Proposed'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('DECLINED', 'Declined'),
    ]

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_appointments'
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_appointments'
    )
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']
        # Ensure no double bookings for doctors
        unique_together = ['doctor', 'date', 'time']

    def __str__(self):
        return f"{self.doctor.get_full_name()} - {self.patient.get_full_name()} ({self.date} {self.time})"
