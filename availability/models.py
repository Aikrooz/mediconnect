from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import DoctorProfileModel,PatientProfileModel,User
# Create your models here.

class AvailabilityModel(models.Model):
    DAY_OF_WEEK=[
        ("Monday","Monday"),
        ("Tuesday","Tuesday"),
        ("Wednesday","Wednesday"),
        ("Thursday","Thursday"),
        ("Friday","Friday"),
        ("Saturday","Saturday"),
        ("Sunday","Sunday")
    ]
    doctor_user=models.ForeignKey(User,related_name="doctor_appointment",on_delete=models.CASCADE)
    day_of_week=models.CharField(choices=DAY_OF_WEEK)
    start_time=models.TimeField()#in the forms widget ,make use of input field should have the type =time
    end_time=models.TimeField()
    slot_duration=models.IntegerField(default=30, help_text="Duration of each Session")
    

    class Meta:
        unique_together=("doctor_user","start_time","end_time","day_of_week")


# The fields can be edited deleted and created therefore a field must be provided for that 

