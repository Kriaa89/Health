from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm
from patients.models import Patient
from doctors.models import Doctor

# Create your views here.

@login_required
def book_appointment(request):
    # Get all doctors
    doctors = Doctor.objects.all()
    
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')
        
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            
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
                patient=request.user.patient,
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
        if request.user != appointment.doctor.user:
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
    if request.user != appointment.patient.user:
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
def appointment_list(request):
    if hasattr(request.user, 'patient'):
        appointments = Appointment.objects.filter(patient=request.user.patient)
    elif hasattr(request.user, 'doctor'):
        appointments = Appointment.objects.filter(doctor=request.user.doctor)
    else:
        appointments = []
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@login_required
def create_appointment(request):
    # Check if user has a patient profile
    if not hasattr(request.user, 'patient'):
        # Create a patient profile if it doesn't exist
        Patient.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            messages.success(request, 'Appointment created successfully!')
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm()
    
    doctors = Doctor.objects.all()
    return render(request, 'appointments/create_appointment.html', {
        'form': form,
        'doctors': doctors
    })
