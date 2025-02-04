from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Nurse(models.Model):
    SPECIALIZATION_CHOICES = [
        ('GENERAL', 'General Nursing'),
        ('PEDIATRIC', 'Pediatric Nursing'),
        ('SURGICAL', 'Surgical Nursing'),
        ('ICU', 'Intensive Care'),
        ('ER', 'Emergency'),
        ('MATERNITY', 'Maternity'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    years_of_experience = models.PositiveIntegerField()
    education = models.TextField()
    certification = models.TextField()
    is_available = models.BooleanField(default=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Nurse {self.user.get_full_name()}"

    class Meta:
        ordering = ['-average_rating']
