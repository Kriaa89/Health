from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('PATIENT', 'Patient'),
    )
    
    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()} - {self.role}"

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    education = models.CharField(max_length=255)
    experience_years = models.IntegerField()
    bio = models.TextField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    languages_spoken = models.CharField(max_length=255)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialty}"

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone = models.CharField(max_length=20)
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Patient: {self.user.get_full_name()}"

class MalePatient(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    prostate_exam = models.BooleanField(default=False)
    psa_level = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    testicular_exam = models.BooleanField(default=False)
    cardiac_test = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FemalePatient(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    last_menstrual = models.DateField(null=True, blank=True)
    mammogram_date = models.DateField(null=True, blank=True)
    pap_smear_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    pregnant = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
    )
    
    TYPE_CHOICES = (
        ('PHYSICAL', 'Physical'),
        ('VIRTUAL', 'Virtual'),
        ('EMERGENCY', 'Emergency'),
        ('HOME', 'Home Visit'),
    )
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    nurse = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='nurse_appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    reason = models.TextField()
    notes = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    symptoms = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    patient_address = models.CharField(max_length=255, blank=True)
    reminder_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment: {self.doctor} with {self.patient} on {self.date}"

class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_reviews')
    nurse = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='nurse_reviews')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Update doctor's average rating when a review is saved
        super().save(*args, **kwargs)
        if self.doctor:
            avg_rating = Review.objects.filter(doctor=self.doctor).aggregate(models.Avg('rating'))['rating__avg']
            total_reviews = Review.objects.filter(doctor=self.doctor).count()
            self.doctor.average_rating = avg_rating
            self.doctor.total_reviews = total_reviews
            self.doctor.save()
