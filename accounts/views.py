from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from appointments.models import Appointment
from .forms import CustomUserCreationForm
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate

# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
        else:
            print("Form errors:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            
            # Redirect based on user role
            if user.role == 'DOCTOR':
                return redirect('doctor_dashboard')
            elif user.role == 'NURSE':
                return redirect('nurse_dashboard')
            elif user.role == 'PATIENT':
                return redirect('patient_dashboard')
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    auth_logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')

@login_required
def doctor_dashboard(request):
    if request.user.role != 'DOCTOR':
        messages.error(request, 'Access denied. You must be a doctor to view this page.')
        return redirect('home')
    
    # Get all appointments for the doctor
    appointments = Appointment.objects.filter(doctor=request.user)
    today = datetime.now().date()
    
    # Get different appointment categories
    pending_appointments = appointments.filter(status='PENDING').order_by('date', 'time')
    upcoming_appointments = appointments.filter(
        status='CONFIRMED',
        date__gte=today
    ).order_by('date', 'time')
    completed_appointments = appointments.filter(status='COMPLETED')
    cancelled_appointments = appointments.filter(status='CANCELLED')
    todays_appointments = appointments.filter(
        date=today
    ).order_by('time')
    
    context = {
        'appointments': appointments,
        'pending_appointments': pending_appointments,
        'upcoming_appointments': upcoming_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'todays_appointments': todays_appointments,
    }
    
    return render(request, 'accounts/doctor_dashboard.html', context)

@login_required
def nurse_dashboard(request):
    if request.user.role != 'NURSE':
        messages.error(request, 'Access denied. You must be a nurse to view this page.')
        return redirect('home')
    return render(request, 'accounts/nurse_dashboard.html')

@login_required
def patient_dashboard(request):
    if request.user.role != 'PATIENT':
        messages.error(request, 'Access denied. You must be a patient to view this page.')
        return redirect('home')
    
    # Get all appointments for the patient
    appointments = Appointment.objects.filter(patient=request.user).order_by('-date', '-time')
    
    # Get appointment counts by status
    upcoming_appointments = appointments.filter(status='CONFIRMED', date__gte=datetime.now().date())
    pending_appointments = appointments.filter(status='PENDING')
    completed_appointments = appointments.filter(status='COMPLETED')
    cancelled_appointments = appointments.filter(status='CANCELLED')
    
    context = {
        'appointments': appointments,
        'upcoming_appointments': upcoming_appointments,
        'pending_appointments': pending_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
    }
    
    return render(request, 'accounts/patient_dashboard.html', context)
