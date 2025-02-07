from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from doctors.models import Doctor
from decimal import Decimal
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Creates 50 sample doctor profiles'

    def handle(self, *args, **kwargs):
        CustomUser = get_user_model()
        
        specialties = [
            'Cardiology', 'Dermatology', 'Endocrinology', 'Family Medicine',
            'Gastroenterology', 'Hematology', 'Internal Medicine', 'Neurology',
            'Obstetrics and Gynecology', 'Oncology', 'Ophthalmology', 'Orthopedics',
            'Pediatrics', 'Psychiatry', 'Pulmonology', 'Radiology', 'Rheumatology',
            'Surgery', 'Urology', 'Emergency Medicine'
        ]
        
        first_names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph',
                      'Thomas', 'Charles', 'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth',
                      'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
                     'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
                     'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']

        created_count = 0
        
        for i in range(50):
            try:
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                email = f"doctor{i+1}_{first_name.lower()}.{last_name.lower()}@example.com"
                
                # Generate a random date of birth (30-70 years ago)
                years_ago = random.randint(30, 70)
                days_variation = random.randint(0, 365)
                date_of_birth = date.today() - timedelta(days=years_ago*365 + days_variation)
                
                # Create CustomUser
                user = CustomUser.objects.create_user(
                    username=f"doctor{i+1}_{first_name.lower()}",
                    email=email,
                    password="Doctor@123",  # Default password
                    first_name=first_name,
                    last_name=last_name,
                    role='DOCTOR',
                    gender=random.choice(['MALE', 'FEMALE']),
                    phone_number=f"+1-555-{str(random.randint(100, 999))}-{str(random.randint(1000, 9999))}",
                    address=f"{random.randint(100, 9999)} Medical Center Drive, Healthcare City",
                    date_of_birth=date_of_birth
                )
                
                # Create Doctor profile
                Doctor.objects.create(
                    user=user,
                    specialty=random.choice(specialties),
                    license_number=f"LIC{str(i+1).zfill(5)}",
                    consultation_fee=Decimal(random.randint(50, 300)),
                    years_of_experience=random.randint(1, 35),
                    education=f"MD from {random.choice(['Harvard Medical School', 'Johns Hopkins School of Medicine', 'Stanford School of Medicine', 'Yale School of Medicine', 'Mayo Medical School'])}",
                    office_address=f"Medical Center {i+1}, Healthcare Street, City",
                    office_hours="Monday-Friday: 9:00 AM - 5:00 PM",
                    is_available=True,
                    average_rating=round(random.uniform(3.5, 5.0), 1),
                    total_reviews=random.randint(0, 100)
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Successfully created doctor: Dr. {first_name} {last_name}'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create doctor {i+1}: {str(e)}'))
                
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} doctor profiles'))
