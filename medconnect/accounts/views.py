from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm
from .models import CustomUser, Doctor, Patient, Appointment, MalePatient, FemalePatient

def home(request):
    return render(request, 'home/index.html')

def role_selection(request):
    return render(request, 'accounts/role_select.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Create specific profile based on role
            if user.role == 'DOCTOR':
                Doctor.objects.create(user=user)
                return redirect('doctor_profile_setup')
            elif user.role == 'PATIENT':
                patient = Patient.objects.create(user=user)
                if user.gender == 'MALE':
                    MalePatient.objects.create(patient=patient)
                else:
                    FemalePatient.objects.create(patient=patient)
                return redirect('patient_profile_setup')
            
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def doctor_dashboard(request):
    if request.user.role != 'DOCTOR':
        messages.error(request, "Access denied. Doctor privileges required.")
        return redirect('home')
    
    doctor = Doctor.objects.get(user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date', 'time')
    
    context = {
        'doctor': doctor,
        'pending_appointments': appointments.filter(status='PENDING'),
        'upcoming_appointments': appointments.filter(status='COMPLETED'),
        'completed_appointments': appointments.filter(status='CANCELED')
    }
    return render(request, 'accounts/doctor_dashboard.html', context)

@login_required
def patient_dashboard(request):
    if request.user.role != 'PATIENT':
        messages.error(request, "Access denied. Patient privileges required.")
        return redirect('home')
    
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('date', 'time')
    
    context = {
        'patient': patient,
        'appointments': appointments
    }
    return render(request, 'accounts/patient_dashboard.html', context)

@login_required
def book_appointment(request):
    if request.user.role != 'PATIENT':
        messages.error(request, "Only patients can book appointments.")
        return redirect('home')
    
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        appointment_type = request.POST.get('type')
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')
        
        doctor = get_object_or_404(Doctor, id=doctor_id)
        patient = Patient.objects.get(user=request.user)
        
        # Create appointment
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            type=appointment_type,
            date=date,
            time=time,
            reason=reason,
            status='PENDING'
        )
        
        messages.success(request, "Appointment request submitted successfully!")
        return redirect('patient_dashboard')
    
    doctors = Doctor.objects.all()
    return render(request, 'accounts/book_appointment.html', {'doctors': doctors})

@login_required
def manage_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Ensure only the relevant doctor can manage the appointment
    if request.user.role == 'DOCTOR' and appointment.doctor.user != request.user:
        messages.error(request, "You can only manage your own appointments.")
        return redirect('doctor_dashboard')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            appointment.status = 'COMPLETED'
            messages.success(request, "Appointment accepted successfully!")
        elif action == 'decline':
            appointment.status = 'CANCELED'
            messages.success(request, "Appointment declined successfully!")
        
        appointment.save()
        return redirect('doctor_dashboard')
    
    return render(request, 'accounts/manage_appointment.html', {'appointment': appointment})

@login_required
def dashboard(request):
    if request.user.role == 'DOCTOR':
        return redirect('doctor_dashboard')
    elif request.user.role == 'NURSE':
        return redirect('nurse_dashboard')
    elif request.user.role == 'PATIENT':
        return redirect('patient_dashboard')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
