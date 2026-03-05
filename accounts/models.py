from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
# Create your models here.
from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    
    ROLE=[
        ("DOCTOR","DOCTOR"),
        ("PATIENT","PATIENT")
    ]

    username=None
    email=models.EmailField(unique=True)
    USERNAME_FIELD='email'
    role=models.CharField(choices=ROLE,default="PATIENT")
    REQUIRED_FIELDS=("role",)
    objects=UserManager()

    class Meta:
        unique_together=('email',"role")


class PatientProfileModel(models.Model):
    GENDER=[
        ("Male","Male"),
        ("Femalte","Female")
    ]
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="patient_user")
    name=models.CharField()
    dob=models.DateField()
    gender=models.CharField(choices=GENDER,default="Male")

class DoctorProfileModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="doctor_user")
    specialities=models.CharField(help_text="Whats you speciality eg.Cardiologist or haemotologis")
    experience=models.PositiveIntegerField(help_text="NUmber of experince in fields")
    consultations_fee=models.PositiveIntegerField()
    bio=models.TextField()
    is_verified=models.BooleanField()

    def get_absolute_url(self):
        return reverse(
            "doctor_detail",
            args=[
                self.id,
            ]
        )

    def __str__(self):
        return self.specialities
    

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Dr. {self.name} - {self.specialty}"