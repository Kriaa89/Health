from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from accounts.models import CustomUser
from datetime import datetime, timedelta

# Create your views here.

@login_required
def book_appointment(request):
    # Get all doctors
    doctors = CustomUser.objects.filter(role='DOCTOR')
    
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')
        
        try:
            doctor = CustomUser.objects.get(id=doctor_id, role='DOCTOR')
            
            # Convert date and time strings to proper format
            appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
            appointment_time = datetime.strptime(time, '%H:%M').time()
            
            # Check if the appointment time is during working hours (8 AM - 5 PM)
            if appointment_time.hour < 8 or appointment_time.hour >= 17:
                messages.error(request, 'Please select a time between 8 AM and 5 PM')
                return redirect('book_appointment')
            
            # Check if doctor already has an appointment at this time
            if Appointment.objects.filter(
                doctor=doctor,
                date=appointment_date,
                time=appointment_time
            ).exists():
                messages.error(request, 'This time slot is already booked. Please select another time.')
                return redirect('book_appointment')
            
            # Create the appointment
            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=request.user,
                date=appointment_date,
                time=appointment_time,
                reason=reason,
                status='PENDING'
            )
            
            messages.success(request, 'Appointment request submitted successfully! Waiting for doctor confirmation.')
            return redirect('patient_dashboard')
            
        except Exception as e:
            messages.error(request, 'Error booking appointment. Please try again.')
            return redirect('book_appointment')
    
    # For GET request, show the booking form
    context = {
        'doctors': doctors,
        'min_date': datetime.now().date().strftime('%Y-%m-%d'),
        'max_date': (datetime.now() + timedelta(days=30)).date().strftime('%Y-%m-%d')
    }
    return render(request, 'appointments/book_appointment.html', context)

@login_required
def manage_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Only the doctor of the appointment can manage it
        if request.user != appointment.doctor:
            messages.error(request, 'You are not authorized to manage this appointment.')
            return redirect('doctor_dashboard')
        
        action = request.POST.get('action')
        
        if action == 'confirm':
            appointment.status = 'CONFIRMED'
            messages.success(request, 'Appointment confirmed successfully!')
        elif action == 'complete':
            appointment.status = 'COMPLETED'
            messages.success(request, 'Appointment marked as completed!')
        elif action == 'cancel':
            appointment.status = 'CANCELLED'
            messages.success(request, 'Appointment cancelled successfully!')
        
        appointment.save()
        
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found.')
    
    return redirect('doctor_dashboard')

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Only allow cancellation if user is the patient and appointment is pending or confirmed
    if request.user != appointment.patient:
        messages.error(request, 'You are not authorized to cancel this appointment.')
        return redirect('patient_dashboard')
    
    if appointment.status not in ['PENDING', 'CONFIRMED']:
        messages.error(request, 'This appointment cannot be cancelled.')
        return redirect('patient_dashboard')
    
    # Cancel the appointment
    appointment.status = 'CANCELLED'
    appointment.save()
    
    messages.success(request, 'Appointment cancelled successfully.')
    return redirect('patient_dashboard')

@login_required
def doctor_schedule(request):
    if request.user.role != 'DOCTOR':
        messages.error(request, 'Access denied. Only doctors can view their schedule.')
        return redirect('accounts:home')
    
    appointments = Appointment.objects.filter(doctor=request.user).order_by('date', 'time')
    return render(request, 'appointments/doctor_schedule.html', {'appointments': appointments})

@login_required
def new_appointment(request):
    if request.user.role != 'DOCTOR':
        messages.error(request, 'Access denied. Only doctors can create new appointments.')
        return redirect('accounts:home')
    
    if request.method == 'POST':
        # Add appointment creation logic here
        pass
    return render(request, 'appointments/new_appointment.html')

@login_required
def patient_records(request):
    if request.user.role != 'DOCTOR':
        messages.error(request, 'Access denied. Only doctors can view patient records.')
        return redirect('accounts:home')
    
    # Get all patients who have had appointments with this doctor
    patients = CustomUser.objects.filter(
        patient_appointments__doctor=request.user
    ).distinct()
    return render(request, 'appointments/patient_records.html', {'patients': patients})
