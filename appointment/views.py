from django.shortcuts import render
from .models import AppointmentModel
from .forms import AppointmentForm
from account.models import DoctorProfileModel
# Create your views here.

def book_appointment(request,doctor_id):
    patient=request.user
    form=AppointmentForm(request.POST)
    if method.POST =="POST":
       if form.is_valid():
        doctor=form.save(commit=False)
        doctor_detail=get_object_or_404(DoctorProfileModel,id=doctor_id)
        doctor_user=doctor_detail.user


