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
    doctor_user=models.ForeignKey(DoctorProfileModel,related_name="doctor_appointment",on_delete=models.CASCADE)
    day_of_week=models.CharField(choices=DAY_OF_WEEK)
    start_time=models.TimeField()#in the forms widget ,make use of input field should have the type =time
    end_time=models.TimeField()
    slot_duration=models.IntegerField(default=30, help_text="Duration of each Session")
    

    class Meta:
        unique_together=("doctor_user","start_time","end_time","day_of_week")


class DoctorAvailability(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    doctor = models.ForeignKey('accounts.Doctor', on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration = models.IntegerField(default=30, help_text="Duration in minutes")
    
    class Meta:
        verbose_name_plural = "Doctor Availabilities"
    
    def __str__(self):
        return f"{self.doctor.name} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


# The fields can be edited deleted and created therefore a field must be provided for that 

