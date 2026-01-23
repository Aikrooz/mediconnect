from django.db import models

from account.models import DoctorProfileModel,PatientModel
# Create your models here.

class AppointmentModel(model.Model):
    doctor=models.ForeignKey(DoctorProfileModel,on_delete=models.CASCADE,related_name="doctor_appointement")
    patient=models.ForeignKey(PatientProfileModel,on_delete=models.CASCADE,related_name="patient_appointment")
    book=models.BooleanField(defualt=False)
    


