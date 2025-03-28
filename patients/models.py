from django.db import models
from accounts.models import CustomUser
from appointments.models import Appointment

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
    
    # Medical history fields - consolidated from gender-specific models
    is_male = models.BooleanField(default=True)
    
    # Common fields for all patients
    last_checkup = models.DateField(null=True, blank=True)
    
    # Male-specific fields
    prostate_exam = models.BooleanField(default=False, null=True, blank=True)
    cardiac_test = models.BooleanField(default=False, null=True, blank=True)
    psa_level = models.FloatField(null=True, blank=True)
    
    # Female-specific fields
    pregnant = models.BooleanField(default=False, null=True, blank=True)
    last_menstrual = models.DateField(null=True, blank=True)
    mammogram_date = models.DateField(null=True, blank=True)
    pap_smear_date = models.DateField(null=True, blank=True)
    gynecological_history = models.TextField(blank=True)

    def __str__(self):
        return f"Patient {self.user.get_full_name()}"
        
    @property
    def medical_info(self):
        """Return relevant medical information based on gender."""
        info = {
            'blood_type': self.blood_type,
            'allergies': self.allergies if self.allergies else None,
            'chronic_conditions': self.chronic_conditions if self.chronic_conditions else None,
            'last_checkup': self.last_checkup
        }
        
        if self.is_male:
            info.update({
                'prostate_exam': self.prostate_exam,
                'cardiac_test': self.cardiac_test,
                'psa_level': self.psa_level
            })
        else:
            info.update({
                'pregnant': self.pregnant,
                'last_menstrual': self.last_menstrual,
                'mammogram_date': self.mammogram_date,
                'pap_smear_date': self.pap_smear_date
            })
            
        return info

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reviews')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='reviews')
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.patient.user.get_full_name()}"

    class Meta:
        ordering = ['-created_at']
