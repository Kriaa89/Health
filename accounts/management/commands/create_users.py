from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import datetime

CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Create sample doctors and patients'

    def handle(self, *args, **kwargs):
        # Male Doctors
        male_doctors = [
            'ahmedbenali@medconnect.com',
            'mohamedtrabelsi@medconnect.com',
            'youssefbouazizi@medconnect.com',
            'karimgharbi@medconnect.com',
            'slimchahed@medconnect.com',
            'hamzabelhadj@medconnect.com',
            'omarmansouri@medconnect.com',
            'ziedkhelifi@medconnect.com',
            'nizarmejri@medconnect.com',
            'wassimjebali@medconnect.com'
        ]

        # Female Doctors
        female_doctors = [
            'leilabensalem@medconnect.com',
            'fatmachakroun@medconnect.com',
            'amirarezgui@medconnect.com',
            'raniahamdi@medconnect.com',
            'yasminemaalej@medconnect.com',
            'nourbelhaj@medconnect.com',
            'ineschebbi@medconnect.com',
            'mariemdridi@medconnect.com',
            'sarrabouslama@medconnect.com',
            'asmalaabidi@medconnect.com'
        ]

        # Patients
        patients = [
            'alimansour@gmail.com',
            'samibrahmi@gmail.com',
            'riadhjelassi@gmail.com',
            'mehdisaidi@gmail.com',
            'bilelamri@gmail.com',
            'rimbelhadj@gmail.com',
            'salmaghariani@gmail.com',
            'emnamiled@gmail.com',
            'hibasassi@gmail.com',
            'nadiaoueslati@gmail.com'
        ]

        # Create male doctors
        for email in male_doctors:
            username = email.split('@')[0]
            first_name = username[:1].upper() + username[1:]
            try:
                CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password='DoctorPass123!',
                    first_name=first_name,
                    gender='MALE',
                    role='DOCTOR',
                    phone_number='12345678',
                    address='Tunisia',
                    date_of_birth='1980-01-01'
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created doctor {email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create doctor {email}: {str(e)}'))

        # Create female doctors
        for email in female_doctors:
            username = email.split('@')[0]
            first_name = username[:1].upper() + username[1:]
            try:
                CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password='DoctorPass123!',
                    first_name=first_name,
                    gender='FEMALE',
                    role='DOCTOR',
                    phone_number='12345678',
                    address='Tunisia',
                    date_of_birth='1980-01-01'
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created doctor {email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create doctor {email}: {str(e)}'))

        # Create patients
        for email in patients:
            username = email.split('@')[0]
            first_name = username[:1].upper() + username[1:]
            gender = 'FEMALE' if any(name in username.lower() for name in ['rim', 'salma', 'emna', 'hiba', 'nadia']) else 'MALE'
            try:
                CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password='PatientPass123!',
                    first_name=first_name,
                    gender=gender,
                    role='PATIENT',
                    phone_number='12345678',
                    address='Tunisia',
                    date_of_birth='1990-01-01'
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created patient {email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create patient {email}: {str(e)}'))
