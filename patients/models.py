from django.db import models
from accounts.models import CustomUser

class Patient(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    emergency_contact_relationship = models.CharField(max_length=50)
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Patient {self.user.get_full_name()}"

class MalePatient(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    prostate_exam = models.BooleanField(default=False)
    cardiac_test = models.BooleanField(default=False)
    psa_level = models.FloatField(null=True, blank=True)
    last_checkup = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Male Patient {self.patient.user.get_full_name()}"

class FemalePatient(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    pregnant = models.BooleanField(default=False)
    last_menstrual = models.DateField(null=True, blank=True)
    mammogram_date = models.DateField(null=True, blank=True)
    pap_smear_date = models.DateField(null=True, blank=True)
    gynecological_history = models.TextField(blank=True)

    def __str__(self):
        return f"Female Patient {self.patient.user.get_full_name()}"

class Appointment(models.Model):
    TYPE_CHOICES = [
        ('PHYSICAL', 'In-Clinic Visit'),
        ('VIRTUAL', 'Virtual Consultation'),
        ('HOME', 'Home Visit'),
        ('EMERGENCY', 'Emergency'),
    ]
    
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
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    symptoms = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    home_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.doctor.user.get_full_name()} ({self.date})"

    class Meta:
        ordering = ['-date', '-time']

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, null=True, blank=True)
    nurse = models.ForeignKey('nurses.Nurse', on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.patient.user.get_full_name()}"

    class Meta:
        ordering = ['-created_at']
