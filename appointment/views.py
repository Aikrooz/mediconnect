from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta, date, time
from .models import Doctor, DoctorAvailability, Appointment
import calendar

@login_required
def book_appointment(request):
    # Get all doctors
    doctors = Doctor.objects.all()
    
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        selected_date = request.POST.get('date')
        
        if not doctor_id or not selected_date:
            messages.error(request, "Please select a doctor and date")
            return redirect('book_appointment')
        
        # Store in session for next step
        request.session['booking_doctor_id'] = doctor_id
        request.session['booking_date'] = selected_date
        return redirect('select_time')
    
    # Generate next 30 days
    today = timezone.now().date()
    date_options = [(today + timedelta(days=i)).strftime('%Y-%m-%d') 
                   for i in range(1, 31)]
    
    return render(request, 'booking/select_doctor.html', {
        'doctors': doctors,
        'date_options': date_options,
        'min_date': (today + timedelta(days=1)).strftime('%Y-%m-%d'),
        'max_date': (today + timedelta(days=30)).strftime('%Y-%m-%d'),
    })

@login_required
def select_time(request):
    doctor_id = request.session.get('booking_doctor_id')
    booking_date = request.session.get('booking_date')
    
    if not doctor_id or not booking_date:
        messages.error(request, "Please start booking from the beginning")
        return redirect('book_appointment')
    
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        booking_date_obj = datetime.strptime(booking_date, '%Y-%m-%d').date()
        day_of_week = booking_date_obj.weekday()  # 0=Monday, 6=Sunday
        
        # Get doctor's availability for this day of week
        availability = DoctorAvailability.objects.filter(
            doctor=doctor, 
            day_of_week=day_of_week
        ).first()
        
        if not availability:
            messages.error(request, "Doctor is not available on this day")
            return redirect('book_appointment')
        
        # Generate time slots
        time_slots = generate_time_slots(availability, booking_date_obj)
        
        if request.method == 'POST':
            selected_time = request.POST.get('time')
            reason = request.POST.get('reason', '')
            
            if not selected_time:
                messages.error(request, "Please select a time slot")
                return render(request, 'booking/select_time.html', {
                    'doctor': doctor,
                    'date': booking_date_obj,
                    'time_slots': time_slots,
                })
            
            # Create appointment
            appointment = Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                date=booking_date_obj,
                time=datetime.strptime(selected_time, '%H:%M').time(),
                reason=reason,
                status='pending'
            )
            
            # Clear session
            request.session.pop('booking_doctor_id', None)
            request.session.pop('booking_date', None)
            
            messages.success(request, "Appointment booked successfully! Waiting for confirmation.")
            return redirect('my_appointments')
        
        return render(request, 'booking/select_time.html', {
            'doctor': doctor,
            'date': booking_date_obj,
            'time_slots': time_slots,
        })
        
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('book_appointment')

def generate_time_slots(availability, booking_date):
    """Generate available time slots based on doctor's availability and existing bookings"""
    slots = []
    current_time = availability.start_time
    end_time = availability.end_time
    
    # Convert to datetime for easier manipulation
    current_datetime = datetime.combine(booking_date, current_time)
    end_datetime = datetime.combine(booking_date, end_time)
    
    # Get existing appointments for this doctor on this date
    existing_appointments = Appointment.objects.filter(
        doctor=availability.doctor,
        date=booking_date,
        status__in=['pending', 'confirmed']
    ).values_list('time', flat=True)
    
    while current_datetime + timedelta(minutes=availability.slot_duration) <= end_datetime:
        slot_time = current_datetime.time()
        
        # Check if slot is available (not booked)
        if slot_time not in existing_appointments:
            slots.append({
                'time': slot_time.strftime('%H:%M'),
                'display': slot_time.strftime('%I:%M %p'),
                'available': True
            })
        else:
            slots.append({
                'time': slot_time.strftime('%H:%M'),
                'display': slot_time.strftime('%I:%M %p'),
                'available': False
            })
        
        current_datetime += timedelta(minutes=availability.slot_duration)
    
    return slots

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('-date', '-time')
    return render(request, 'booking/my_appointments.html', {
        'appointments': appointments
    })

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    
    # Check if appointment is at least 24 hours away
    appointment_datetime = datetime.combine(appointment.date, appointment.time)
    if timezone.now() + timedelta(hours=24) > appointment_datetime:
        messages.error(request, "Cannot cancel within 24 hours of appointment")
    else:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, "Appointment cancelled successfully")
    
    return redirect('my_appointments')

# Staff/Admin Views
@login_required
def manage_appointments(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied")
        return redirect('index')
    
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')
    
    appointments = Appointment.objects.all()
    
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    if date_filter:
        appointments = appointments.filter(date=date_filter)
    
    return render(request, 'booking/manage_appointments.html', {
        'appointments': appointments.order_by('date', 'time'),
        'status_choices': Appointment.STATUS_CHOICES,
    })

@login_required
def update_appointment_status(request, appointment_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied")
        return redirect('index')
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            messages.success(request, f"Appointment status updated to {new_status}")
    
    return redirect('manage_appointments')

from django.shortcuts import render, get_object_or_404

def index(request):
    """Homepage"""
    return render(request, 'booking/index.html')

def doctor_list(request):
    """List all doctors"""
    doctors = Doctor.objects.all()
    return render(request, 'booking/doctor_list.html', {'doctors': doctors})

def doctor_detail(request, doctor_id):
    """Show doctor details and their availability"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    availabilities = doctor.availabilities.all()
    return render(request, 'booking/doctor_detail.html', {
        'doctor': doctor,
        'availabilities': availabilities
    })