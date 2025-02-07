from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from accounts.models import CustomUser
from datetime import datetime, timedelta
import random

# Create your views here.

@login_required
def book_appointment(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')
        doctor_id = request.POST.get('doctor')
        
        try:
            # Convert date string to proper format
            appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
            # Convert time string to proper format
            appointment_time = datetime.strptime(time, '%H:%M').time()
            
            # Get the selected doctor
            doctor = get_object_or_404(CustomUser, id=doctor_id, role='DOCTOR')
            
            # Check if the doctor already has an appointment at this time
            existing_appointment = Appointment.objects.filter(
                doctor=doctor,
                date=appointment_date,
                time=appointment_time
            ).exists()
            
            if existing_appointment:
                messages.error(request, 'This time slot is already booked. Please choose another time.')
                return redirect('appointments:book_appointment')
            
            # Create the appointment with time
            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=request.user,
                date=appointment_date,
                time=appointment_time,
                reason=reason,
                status='PENDING'
            )
            
            messages.success(request, 'Appointment request submitted successfully! Please wait for doctor confirmation.')
            return redirect('accounts:patient_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error booking appointment: {str(e)}')
            return redirect('appointments:book_appointment')
    
    # For GET request, show the booking form with available doctors
    doctors = CustomUser.objects.filter(role='DOCTOR')
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
        
        # Check if user is either the doctor or the patient
        if request.user != appointment.doctor and request.user != appointment.patient:
            messages.error(request, 'You are not authorized to manage this appointment.')
            return redirect('accounts:home')
        
        action = request.POST.get('action')
        
        if action == 'propose_time' and request.user == appointment.doctor:
            appointment_time = request.POST.get('appointment_time')
            if not appointment_time:
                messages.error(request, 'Please select an appointment time.')
                return redirect('appointments:doctor_schedule')
            
            try:
                # Convert time string to proper format
                time_obj = datetime.strptime(appointment_time, '%H:%M').time()
                
                # Check if the time is during working hours (8 AM - 5 PM)
                if time_obj.hour < 8 or time_obj.hour >= 17:
                    messages.error(request, 'Please select a time between 8 AM and 5 PM')
                    return redirect('appointments:doctor_schedule')
                
                # Check if doctor already has an appointment at this time
                if Appointment.objects.filter(
                    doctor=request.user,
                    date=appointment.date,
                    time=time_obj,
                    status='CONFIRMED'
                ).exists():
                    messages.error(request, 'You already have an appointment at this time.')
                    return redirect('appointments:doctor_schedule')
                
                appointment.time = time_obj
                appointment.status = 'TIME_PROPOSED'
                messages.success(request, 'Appointment time proposed. Waiting for patient confirmation.')
                
            except ValueError:
                messages.error(request, 'Invalid time format.')
                return redirect('appointments:doctor_schedule')
        
        elif action == 'accept_time' and request.user == appointment.patient:
            if appointment.status == 'TIME_PROPOSED':
                appointment.status = 'CONFIRMED'
                messages.success(request, 'Appointment time accepted and confirmed!')
            else:
                messages.error(request, 'This appointment is no longer awaiting time confirmation.')
        
        elif action == 'decline_time' and request.user == appointment.patient:
            if appointment.status == 'TIME_PROPOSED':
                appointment.status = 'DECLINED'
                appointment.time = None
                messages.success(request, 'Appointment time declined. The doctor will be notified.')
            else:
                messages.error(request, 'This appointment is no longer awaiting time confirmation.')
        
        elif action == 'complete' and request.user == appointment.doctor:
            if appointment.status == 'CONFIRMED':
                appointment.status = 'COMPLETED'
                messages.success(request, 'Appointment marked as completed!')
            else:
                messages.error(request, 'Only confirmed appointments can be marked as completed.')
        
        elif action == 'cancel':
            if request.user == appointment.doctor or request.user == appointment.patient:
                appointment.status = 'CANCELLED'
                messages.success(request, 'Appointment cancelled successfully!')
            else:
                messages.error(request, 'You are not authorized to cancel this appointment.')
        
        appointment.save()
        
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found.')
    
    # Redirect based on user role
    if request.user == appointment.doctor:
        return redirect('appointments:doctor_schedule')
    else:
        return redirect('accounts:patient_dashboard')

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Only allow cancellation if user is the patient and appointment is pending or confirmed
    if request.user != appointment.patient:
        messages.error(request, 'You are not authorized to cancel this appointment.')
        return redirect('accounts:patient_dashboard')
    
    if appointment.status not in ['PENDING', 'CONFIRMED']:
        messages.error(request, 'This appointment cannot be cancelled.')
        return redirect('accounts:patient_dashboard')
    
    # Cancel the appointment
    appointment.status = 'CANCELLED'
    appointment.save()
    
    messages.success(request, 'Appointment cancelled successfully.')
    return redirect('accounts:patient_dashboard')

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

@login_required
def delete_appointment(request, appointment_id):
    if request.user.role != 'DOCTOR':
        messages.error(request, 'Access denied. Only doctors can delete appointments.')
        return redirect('accounts:home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if the appointment belongs to the doctor
    if appointment.doctor != request.user:
        messages.error(request, 'Access denied. You can only delete your own appointments.')
        return redirect('accounts:doctor_dashboard')
    
    # Delete the appointment
    appointment.delete()
    messages.success(request, 'Appointment deleted successfully.')
    return redirect('accounts:doctor_dashboard')
