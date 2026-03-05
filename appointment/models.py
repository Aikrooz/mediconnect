from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import DoctorProfileModel,PatientProfileModel
from availability.models import AvailabilityModel

User = get_user_model()
# Create your models here.


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey('accounts.Doctor', on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['doctor', 'date', 'time']
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.patient.username} with Dr. {self.doctor.name} on {self.date} at {self.time}"
