import os
import django
import random
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medconnect.settings')
django.setup()

from accounts.models import CustomUser

# Lists for generating realistic data
first_names_male = [
    'Ahmed', 'Mohamed', 'Ali', 'Omar', 'Youssef', 'Ibrahim', 'Hassan', 'Karim', 'Amir', 'Zied',
    'Mehdi', 'Slim', 'Habib', 'Nizar', 'Sami', 'Tarek', 'Walid', 'Hichem', 'Bilel', 'Hamza',
    'Amine', 'Aymen', 'Wassim', 'Hatem', 'Ramzi'
]

first_names_female = [
    'Sarah', 'Fatma', 'Mariem', 'Nour', 'Amira', 'Ines', 'Yasmine', 'Rania', 'Asma', 'Lina',
    'Sarra', 'Rim', 'Emna', 'Aya', 'Salma', 'Malak', 'Yosra', 'Ghada', 'Hiba', 'Rihab',
    'Sirine', 'Rahma', 'Farah', 'Chaima', 'Wafa'
]

last_names = [
    'Ben Ali', 'Ben Ahmed', 'Ben Salah', 'Ben Ammar', 'Ben Youssef', 'Trabelsi', 'Bouazizi',
    'Gharbi', 'Mejri', 'Tlili', 'Hamdi', 'Sassi', 'Dridi', 'Chebbi', 'Mansouri', 'Jebali',
    'Khemiri', 'Rezgui', 'Maalej', 'Belhadj', 'Mbarek', 'Riahi', 'Nasri', 'Jelassi', 'Lahmar'
]

# Function to generate a random Tunisian phone number
def generate_phone():
    return f"{random.randint(20000000, 99999999)}"

# Function to generate a random date of birth (30-65 years old)
def generate_dob():
    today = datetime.now()
    age = random.randint(30, 65)
    days_variation = random.randint(0, 365)
    return (today - timedelta(days=age*365 + days_variation)).date()

# Function to generate a random address in Tunisia
def generate_address():
    cities = ['Tunis', 'Sfax', 'Sousse', 'Kairouan', 'Bizerte', 'Gabès', 'Ariana', 'Gafsa', 'Monastir', 'Ben Arous']
    streets = ['Avenue Habib Bourguiba', 'Rue de la République', 'Avenue de la Liberté', 'Rue Ibn Khaldoun', 'Avenue de Paris']
    return f"{random.randint(1, 100)} {random.choice(streets)}, {random.choice(cities)}, Tunisia"

# Create 50 doctors (25 male, 25 female)
def create_doctors():
    created_count = 0
    
    # Create 25 male doctors
    for i in range(25):
        first_name = random.choice(first_names_male)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower().replace(' ', '')}@medconnect.tn"
        
        try:
            doctor = CustomUser.objects.create_user(
                username=email,
                email=email,
                password="Doctor123!",  # Default password
                first_name=first_name,
                last_name=last_name,
                gender='MALE',
                role='DOCTOR',
                phone_number=generate_phone(),
                address=generate_address(),
                date_of_birth=generate_dob()
            )
            print(f"Created male doctor: {doctor.get_full_name()}")
            created_count += 1
        except Exception as e:
            print(f"Error creating male doctor: {e}")
    
    # Create 25 female doctors
    for i in range(25):
        first_name = random.choice(first_names_female)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower().replace(' ', '')}@medconnect.tn"
        
        try:
            doctor = CustomUser.objects.create_user(
                username=email,
                email=email,
                password="Doctor123!",  # Default password
                first_name=first_name,
                last_name=last_name,
                gender='FEMALE',
                role='DOCTOR',
                phone_number=generate_phone(),
                address=generate_address(),
                date_of_birth=generate_dob()
            )
            print(f"Created female doctor: {doctor.get_full_name()}")
            created_count += 1
        except Exception as e:
            print(f"Error creating female doctor: {e}")
    
    print(f"\nTotal doctors created: {created_count}")
    print("Default password for all doctors: Doctor123!")

if __name__ == '__main__':
    print("Starting to create doctors...")
    create_doctors()
    print("Finished creating doctors!")
