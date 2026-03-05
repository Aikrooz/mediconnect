from django.shortcuts import render
from .models import AppointmentModel
from accounts.models import DoctorProfileModel
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from .models import AppointmentModel, DoctorProfileModel





