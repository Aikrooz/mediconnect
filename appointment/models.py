from django.db import models

from accounts.models import DoctorProfileModel,PatientProfileModel
from availability.models import AvailabilityModel
# Create your models here.

class AppointmentModel(models.Model):

    STATUS=[
        ('Pending','Pending'),
        ('Confirmation','Confirmation'),
        ('Cancelled','Cancelled'),
        ('Completed','Completed')
    ]

    doctor=models.ForeignKey(DoctorProfileModel,on_delete=models.CASCADE,related_name="doctor_appointement")
    patient=models.ForeignKey(PatientProfileModel,on_delete=models.CASCADE,related_name="patient_appointment")
    slot=models.ForeignKey(AvailabilityModel,on_delete=models.CASCADE,related_name="available_slot")
    status=models.CharField(choices=STATUS,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
class Meta:
    unique_together = ['doctor', 'date', 'slot']
    ordering=["date","slot"]
