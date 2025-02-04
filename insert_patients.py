import os
import django
import random
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medconnect.settings')
django.setup()

from accounts.models import CustomUser
from appointments.models import Appointment

# Lists for generating realistic data
first_names_male = [
    'Mohamed', 'Ahmed', 'Ali', 'Omar', 'Youssef', 'Amine', 'Aymen', 'Bilel', 'Chiheb', 'Elyes',
    'Fares', 'Ghaith', 'Hamza', 'Iheb', 'Issam', 'Jawher', 'Kamel', 'Lotfi', 'Maher', 'Nabil',
    'Oussama', 'Qaiss', 'Rami', 'Saif', 'Taher', 'Wael', 'Yassine', 'Zouheir', 'Achref', 'Badr',
    'Chahine', 'Dhia', 'Ezeddine', 'Farouk', 'Ghassen', 'Haythem', 'Ilyes', 'Jasser', 'Khalil',
    'Mehdi', 'Nadim', 'Ouael', 'Rached', 'Saber', 'Taha', 'Wassim', 'Yacine', 'Zied', 'Aziz', 'Bassem'
]

first_names_female = [
    'Amira', 'Asma', 'Cyrine', 'Dorra', 'Emna', 'Fatma', 'Ghada', 'Hajer', 'Ines', 'Jihen',
    'Khouloud', 'Lamia', 'Mariem', 'Nour', 'Olfa', 'Rahma', 'Sabrine', 'Takwa', 'Wafa', 'Yosra',
    'Zeineb', 'Abir', 'Balkis', 'Chaima', 'Dalia', 'Eya', 'Farah', 'Ghofrane', 'Hiba', 'Ichrak',
    'Jalila', 'Kawther', 'Lina', 'Maram', 'Nawres', 'Oumaima', 'Rim', 'Salma', 'Tasnim', 'Wissal',
    'Yasmine', 'Zahra', 'Afef', 'Bochra', 'Dorsaf', 'Essia', 'Ferdaous', 'Houda', 'Ikram', 'Jinene'
]

last_names = [
    'Ben Ali', 'Ben Ahmed', 'Ben Salah', 'Ben Ammar', 'Ben Youssef', 'Trabelsi', 'Bouazizi',
    'Gharbi', 'Mejri', 'Tlili', 'Hamdi', 'Sassi', 'Dridi', 'Chebbi', 'Mansouri', 'Jebali',
    'Khemiri', 'Rezgui', 'Maalej', 'Belhadj', 'Mbarek', 'Riahi', 'Nasri', 'Jelassi', 'Lahmar',
    'Ben Abdallah', 'Ben Hassine', 'Ben Othman', 'Ben Slimane', 'Chaabane', 'Derbali', 'Feki',
    'Guermazi', 'Hammami', 'Jlassi', 'Kammoun', 'Laabidi', 'Masmoudi', 'Nafti', 'Oueslati',
    'Rebai', 'Sfaxi', 'Tounsi', 'Zaidi', 'Ben Amor', 'Ben Brahim', 'Ben Hamida', 'Ben Mansour',
    'Ben Romdhane', 'Chouchane'
]

# Function to generate a random Tunisian phone number
def generate_phone():
    return f"{random.randint(20000000, 99999999)}"

# Function to generate a random date of birth (18-80 years old)
def generate_dob():
    today = datetime.now()
    age = random.randint(18, 80)
    days_variation = random.randint(0, 365)
    return (today - timedelta(days=age*365 + days_variation)).date()

# Function to generate a random address in Tunisia
def generate_address():
    cities = [
        'Tunis', 'Sfax', 'Sousse', 'Kairouan', 'Bizerte', 'Gabès', 'Ariana', 'Gafsa', 
        'Monastir', 'Ben Arous', 'La Marsa', 'Medenine', 'Nabeul', 'Moknine', 'Djerba', 
        'Hammamet', 'Tataouine', 'Tozeur', 'Siliana', 'Kebili'
    ]
    streets = [
        'Avenue Habib Bourguiba', 'Rue de la République', 'Avenue de la Liberté', 
        'Rue Ibn Khaldoun', 'Avenue de Paris', 'Rue Charles de Gaulle', 
        'Avenue Mohamed V', 'Rue Ali Belhouane', 'Avenue Farhat Hached',
        'Rue des Martyrs'
    ]
    return f"{random.randint(1, 100)} {random.choice(streets)}, {random.choice(cities)}, Tunisia"

# Create 100 patients (50 male, 50 female)
def create_patients():
    created_count = 0
    
    # Create 50 male patients
    for i in range(50):
        first_name = random.choice(first_names_male)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower().replace(' ', '')}@gmail.com"
        
        try:
            patient = CustomUser.objects.create_user(
                username=email,
                email=email,
                password="Patient123!",  # Default password
                first_name=first_name,
                last_name=last_name,
                gender='MALE',
                role='PATIENT',
                phone_number=generate_phone(),
                address=generate_address(),
                date_of_birth=generate_dob()
            )
            print(f"Created male patient: {patient.get_full_name()}")
            created_count += 1
        except Exception as e:
            print(f"Error creating male patient: {e}")
    
    # Create 50 female patients
    for i in range(50):
        first_name = random.choice(first_names_female)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower().replace(' ', '')}@gmail.com"
        
        try:
            patient = CustomUser.objects.create_user(
                username=email,
                email=email,
                password="Patient123!",  # Default password
                first_name=first_name,
                last_name=last_name,
                gender='FEMALE',
                role='PATIENT',
                phone_number=generate_phone(),
                address=generate_address(),
                date_of_birth=generate_dob()
            )
            print(f"Created female patient: {patient.get_full_name()}")
            created_count += 1
        except Exception as e:
            print(f"Error creating female patient: {e}")

    print(f"\nTotal patients created: {created_count}")
    print("Default password for all patients: Patient123!")

# Create some sample appointments
def create_sample_appointments():
    doctors = CustomUser.objects.filter(role='DOCTOR')
    patients = CustomUser.objects.filter(role='PATIENT')
    
    if not doctors or not patients:
        print("No doctors or patients found. Please create them first.")
        return
    
    appointment_count = 0
    statuses = ['PENDING', 'CONFIRMED', 'COMPLETED']
    reasons = [
        'Regular check-up', 'Follow-up visit', 'Consultation', 'Annual physical',
        'Vaccination', 'Blood test', 'Medical certificate', 'Prescription renewal'
    ]
    
    # Create 200 random appointments
    for _ in range(200):
        doctor = random.choice(doctors)
        patient = random.choice(patients)
        status = random.choice(statuses)
        
        # Generate random date within next 30 days for pending/confirmed
        # or past 30 days for completed
        if status == 'COMPLETED':
            days_offset = random.randint(-30, -1)
        else:
            days_offset = random.randint(1, 30)
        
        appointment_date = datetime.now().date() + timedelta(days=days_offset)
        appointment_time = datetime.strptime(f"{random.randint(8, 17)}:00", "%H:%M").time()
        
        try:
            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                date=appointment_date,
                time=appointment_time,
                status=status,
                reason=random.choice(reasons),
                notes="Sample appointment note" if status == 'COMPLETED' else ""
            )
            appointment_count += 1
            print(f"Created appointment: {appointment}")
        except Exception as e:
            print(f"Error creating appointment: {e}")
    
    print(f"\nTotal appointments created: {appointment_count}")

if __name__ == '__main__':
    print("Starting to create patients...")
    create_patients()
    print("\nCreating sample appointments...")
    create_sample_appointments()
    print("Finished creating test data!")
