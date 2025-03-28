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
            return redirect('accounts:login')
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
        email = request.POST.get('username')  # Form sends email in username field
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            
            # Redirect based on user role
            if user.role == 'DOCTOR':
                return redirect('accounts:doctor_dashboard')
            elif user.role == 'NURSE':
                return redirect('accounts:nurse_dashboard')
            elif user.role == 'PATIENT':
                return redirect('accounts:patient_dashboard')
            else:
                return redirect('accounts:home')
        else:
            messages.error(request, 'Invalid email or password.')
    
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    auth_logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('accounts:home')

@login_required
def doctor_dashboard(request):
    if request.user.role != 'DOCTOR':
        messages.error(request, 'Access denied. You must be a doctor to view this page.')
        return redirect('home')
    
    today = datetime.now().date()
    
    # Use select_related to fetch related patient data in a single query
    # This avoids N+1 query problem when accessing patient information in templates
    base_query = Appointment.objects.filter(doctor=request.user).select_related('patient')
    
    # Limit recent appointments for improved performance
    recent_appointments = base_query.filter(
        status__in=['COMPLETED', 'CANCELLED']
    ).order_by('-date', '-time')[:10]
    
    context = {
        'doctor': request.user,
        'pending_appointments': base_query.filter(status='PENDING').order_by('date', 'time'),
        'time_proposed_appointments': base_query.filter(status='TIME_PROPOSED').order_by('date', 'time'),
        'upcoming_appointments': base_query.filter(
            status='CONFIRMED',
            date__gte=today
        ).order_by('date', 'time'),
        'todays_appointments': base_query.filter(
            date=today,
            status='CONFIRMED'
        ).order_by('time'),
        'recent_appointments': recent_appointments,
    }
    
    # Add appointment counts to avoid extra queries in the template
    context['pending_count'] = context['pending_appointments'].count()
    context['upcoming_count'] = context['upcoming_appointments'].count()
    context['todays_count'] = context['todays_appointments'].count()
    
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
    
    today = datetime.now().date()
    
    # Use select_related to fetch related doctor data in a single query
    # This avoids N+1 query problem when accessing doctor information in templates
    base_query = Appointment.objects.filter(patient=request.user).select_related('doctor')
    
    # Get all appointments for the patient, but limit to 20 most recent for improved performance
    all_appointments = base_query.order_by('-date', '-time')[:20]
    
    # Get appointment counts by status using prefetched base query
    context = {
        'appointments': all_appointments,
        'upcoming_appointments': base_query.filter(status='CONFIRMED', date__gte=today),
        'pending_appointments': base_query.filter(status__in=['PENDING', 'TIME_PROPOSED']),
        'completed_appointments': base_query.filter(status='COMPLETED'),
        'cancelled_appointments': base_query.filter(status__in=['CANCELLED', 'DECLINED']),
        'user': request.user
    }
    
    return render(request, 'accounts/patient_dashboard.html', context)
