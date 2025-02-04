from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    years_of_experience = models.PositiveIntegerField()
    education = models.TextField()
    office_address = models.TextField()
    office_hours = models.TextField()
    is_available = models.BooleanField(default=True)
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

    class Meta:
        ordering = ['-average_rating']
