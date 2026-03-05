from django.shortcuts import render
from .models import AppointmentModel
from accounts.models import DoctorProfileModel
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import AppointmentModel, DoctorProfileModel

@login_required
def appointment(request):
    doctors=DoctorProfileModel.objects.all()
    if request.mehtod=="POST":
        





