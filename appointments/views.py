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
        reason = request.POST.get('reason')
        doctor_id = request.POST.get('doctor')
        appointment_type = request.POST.get('type', 'PHYSICAL')
        symptoms = request.POST.get('symptoms', '')
        
        try:
            # Convert date string to proper format
            appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
            
            # Validate date is not in the past
            if appointment_date < datetime.now().date():
                messages.error(request, 'Cannot book appointments in the past.')
                return redirect('appointments:book_appointment')
            
            # Get the selected doctor (with select_related to avoid extra queries)
            doctor = get_object_or_404(CustomUser, id=doctor_id, role='DOCTOR')
            
            # Create the appointment with new fields from our enhanced model
            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=request.user,
                date=appointment_date,
                time=None,
                reason=reason,
                type=appointment_type,
                symptoms=symptoms,
                status='PENDING'
            )
            
            messages.success(request, 'Appointment request submitted successfully! Please wait for doctor confirmation.')
            return redirect('accounts:patient_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error booking appointment: {str(e)}')
            return redirect('appointments:book_appointment')
    
    # For GET request, show the booking form with available doctors
    # Use values() to optimize the query by only retrieving needed fields
    doctors = CustomUser.objects.filter(role='DOCTOR').order_by('first_name')
    
    context = {
        'doctors': doctors,
        'min_date': datetime.now().date().strftime('%Y-%m-%d'),
        'max_date': (datetime.now() + timedelta(days=30)).date().strftime('%Y-%m-%d'),
        'appointment_types': dict(Appointment.TYPE_CHOICES)
    }
    return render(request, 'appointments/book_appointment.html', context)

@login_required
def manage_appointment(request, appointment_id):
    # Fetch the appointment with related models in one query to reduce database calls
    try:
        appointment = Appointment.objects.select_related('doctor', 'patient').get(id=appointment_id)
        
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
                
                # Check for existing appointments with a single query
                conflicting_appointments = Appointment.objects.filter(
                    doctor=request.user,
                    date=appointment.date,
                    time=time_obj,
                    status='CONFIRMED'
                ).exclude(id=appointment.id).exists()
                
                if conflicting_appointments:
                    messages.error(request, 'You already have an appointment at this time.')
                    return redirect('appointments:doctor_schedule')
                
                appointment.time = time_obj
                appointment.status = 'TIME_PROPOSED'
                messages.success(request, 'Appointment time proposed. Waiting for patient confirmation.')
                
            except ValueError:
                messages.error(request, 'Invalid time format.')
                return redirect('appointments:doctor_schedule')
                
        elif action == 'update_notes' and request.user == appointment.doctor:
            notes = request.POST.get('notes', '')
            diagnosis = request.POST.get('diagnosis', '')
            prescription = request.POST.get('prescription', '')
            
            appointment.notes = notes
            appointment.diagnosis = diagnosis
            appointment.prescription = prescription
            messages.success(request, 'Medical information updated successfully.')
        
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
        return redirect('accounts:home')
    
    # Redirect based on user role
    if request.user == appointment.doctor:
        return redirect('appointments:doctor_schedule')
    else:
        return redirect('accounts:patient_dashboard')

@login_required
def cancel_appointment(request, appointment_id):
    # Use select_related to reduce database queries
    appointment = get_object_or_404(
        Appointment.objects.select_related('patient', 'doctor'), 
        id=appointment_id
    )
    
    # Only allow cancellation if user is the patient and appointment is in a cancellable state
    if request.user != appointment.patient and request.user != appointment.doctor:
        messages.error(request, 'You are not authorized to cancel this appointment.')
        return redirect('accounts:patient_dashboard' if request.user.role == 'PATIENT' else 'accounts:doctor_dashboard')
    
    cancellable_statuses = ['PENDING', 'TIME_PROPOSED', 'CONFIRMED']
    if appointment.status not in cancellable_statuses:
        messages.error(request, 'This appointment cannot be cancelled.')
        return redirect('accounts:patient_dashboard' if request.user.role == 'PATIENT' else 'accounts:doctor_dashboard')
    
    # Cancel the appointment
    appointment.status = 'CANCELLED'
    appointment.save(update_fields=['status', 'updated_at'])  # Only update necessary fields
    
    messages.success(request, 'Appointment cancelled successfully.')
    return redirect('accounts:patient_dashboard' if request.user.role == 'PATIENT' else 'accounts:doctor_dashboard')

@login_required
def doctor_schedule(request):
    if request.user.role != 'DOCTOR':
        messages.error(request, 'Access denied. Only doctors can view their schedule.')
        return redirect('accounts:home')
    
    # Use select_related to avoid N+1 query problem when accessing patient data
    appointments = Appointment.objects.filter(doctor=request.user).select_related('patient').order_by('date', 'time')
    
    # Group appointments by date for better UI organization
    today = datetime.now().date()
    upcoming = {}
    past = {}
    
    for appointment in appointments:
        # Skip cancelled appointments older than 7 days
        if appointment.status == 'CANCELLED' and (today - appointment.date).days > 7:
            continue
            
        if appointment.date >= today:
            if appointment.date not in upcoming:
                upcoming[appointment.date] = []
            upcoming[appointment.date].append(appointment)
        else:
            if appointment.date not in past:
                past[appointment.date] = []
            past[appointment.date].append(appointment)
    
    context = {
        'appointments': appointments,
        'upcoming_dates': sorted(upcoming.keys()),
        'upcoming': upcoming,
        'past_dates': sorted(past.keys(), reverse=True)[:7],  # Only show last 7 days
        'past': past,
        'today': today
    }
    
    return render(request, 'appointments/doctor_schedule.html', context)

@login_required
def new_appointment(request):
    if request.user.role != 'DOCTOR':
        messages.error(request, 'Access denied. Only doctors can create new appointments.')
        return redirect('accounts:home')
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')
        appointment_type = request.POST.get('type', 'PHYSICAL')
        notes = request.POST.get('notes', '')
        
        try:
            # Get the patient
            patient = get_object_or_404(CustomUser, id=patient_id, role='PATIENT')
            
            # Validate date and time
            appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
            if appointment_date < datetime.now().date():
                messages.error(request, 'Cannot book appointments in the past.')
                return redirect('appointments:new_appointment')
            
            appointment_time = None
            if time:
                try:
                    appointment_time = datetime.strptime(time, '%H:%M').time()
                    # Check if the time is during working hours (8 AM - 5 PM)
                    if appointment_time.hour < 8 or appointment_time.hour >= 17:
                        messages.error(request, 'Please select a time between 8 AM and 5 PM')
                        return redirect('appointments:new_appointment')
                    
                    # Check for existing appointments at this time
                    if Appointment.objects.filter(
                        doctor=request.user,
                        date=appointment_date,
                        time=appointment_time,
                        status='CONFIRMED'
                    ).exists():
                        messages.error(request, 'You already have an appointment at this time.')
                        return redirect('appointments:new_appointment')
                except ValueError:
                    messages.error(request, 'Invalid time format.')
                    return redirect('appointments:new_appointment')
            
            # Create the appointment - automatically confirmed if doctor creates it with a time
            status = 'CONFIRMED' if appointment_time else 'PENDING'
            
            appointment = Appointment.objects.create(
                doctor=request.user,
                patient=patient,
                date=appointment_date,
                time=appointment_time,
                reason=reason,
                type=appointment_type,
                notes=notes,
                status=status
            )
            
            messages.success(request, f'Appointment with {patient.get_full_name()} has been created successfully.')
            return redirect('appointments:doctor_schedule')
            
        except Exception as e:
            messages.error(request, f'Error creating appointment: {str(e)}')
            return redirect('appointments:new_appointment')
    
    # For GET request, show form with list of patients
    # Get patients who have had previous appointments with this doctor first
    from django.db.models import Count
    
    previous_patients = CustomUser.objects.filter(
        patient_appointments__doctor=request.user,
        role='PATIENT'
    ).annotate(
        appointment_count=Count('patient_appointments')
    ).order_by('-appointment_count')
    
    # Then get other patients who haven't had appointments with this doctor
    other_patients = CustomUser.objects.filter(
        role='PATIENT'
    ).exclude(
        id__in=previous_patients.values_list('id', flat=True)
    ).order_by('last_name', 'first_name')
    
    context = {
        'previous_patients': previous_patients,
        'other_patients': other_patients,
        'min_date': datetime.now().date().strftime('%Y-%m-%d'),
        'max_date': (datetime.now() + timedelta(days=90)).date().strftime('%Y-%m-%d'),
        'appointment_types': dict(Appointment.TYPE_CHOICES)
    }
    
    return render(request, 'appointments/new_appointment.html', context)

@login_required
def patient_records(request):
    if request.user.role != 'DOCTOR':
        messages.error(request, 'Access denied. Only doctors can view patient records.')
        return redirect('accounts:home')
    
    # Use values and annotate to efficiently get patient data with appointment counts
    from django.db.models import Count, Q
    
    patients = CustomUser.objects.filter(
        patient_appointments__doctor=request.user,
        role='PATIENT'
    ).annotate(
        appointment_count=Count('patient_appointments'),
        completed_count=Count('patient_appointments', 
                             filter=Q(patient_appointments__status='COMPLETED')),
        pending_count=Count('patient_appointments', 
                           filter=Q(patient_appointments__status__in=['PENDING', 'TIME_PROPOSED']))
    ).order_by('-patient_appointments__date').distinct()
    
    context = {
        'patients': patients,
        'today': datetime.now().date()
    }
    
    return render(request, 'appointments/patient_records.html', context)

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
