from django.db import models
from django.conf import settings

# Create your models here.

class Appointment(models.Model):
    TYPE_CHOICES = [
        ('PHYSICAL', 'In-Clinic Visit'),
        ('VIRTUAL', 'Virtual Consultation'),
        ('HOME', 'Home Visit'),
        ('EMERGENCY', 'Emergency'),
    ]
    
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
    
    # Added fields from the old patients.Appointment model
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='PHYSICAL')
    reason = models.TextField()
    symptoms = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    home_address = models.TextField(blank=True, null=True)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']
        # More precise constraint to handle null times (pending appointments)
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date', 'time'],
                condition=models.Q(time__isnull=False),
                name='unique_appointment_when_time_set'
            )
        ]

    def __str__(self):
        return f"{self.doctor.get_full_name()} - {self.patient.get_full_name()} ({self.date} {self.time if self.time else 'No time set'})"
