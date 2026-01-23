from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import TemplateView
from availability.models import AvailabilityModel
from .forms import DoctorProfileForm, PatientProfileForm, UserCreationForm, LoginForm
from .models import User,DoctorProfileModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

def create_user(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()

            if user.role == "DOCTOR":
                return redirect("doctor_profile")   
            else:
                return redirect("patient_profile")
    else:
        user_form = UserCreationForm()

    return render(
        request,
        "registration/register_user.html",
        {"user": user_form}
    )



@login_required
def create_doctor_profile(request):
    user = request.user

    if request.method == "POST":
        form = DoctorProfileForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.user = user       
            doctor.is_verified = False
            doctor.save()

            return redirect("doctor_homepage")
    else:
        form = DoctorProfileForm()

    return render(
        request,
        "registration/doctor_profile.html",
        {"form": form}
    )


@login_required
def create_patient_profile(request):
    user = request.user

    if request.method == "POST":
        form = PatientProfileForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = user      
            patient.save()

            return redirect("patient_homepage")
    else:
        form = PatientProfileForm()

    return render(
        request,
        "registration/patient_profile.html",
        {"form": form}
    )


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user:
            login(request, user)

            if user.role == "DOCTOR":
                return redirect("doctor_homepage")
            else:
                return redirect("patient_homepage")

        return render(
            request,
            "registration/login.html",
            {"form": form, "error": "Invalid credentials"}
        )

    return render(request, "registration/login.html", {"form": form})

from availability.models import AvailabilityModel

@login_required
def doctor_homepage(request):
    user = request.user
    print(user.doctor_appointment.all())
    availabilities=user.doctor_appointment.all()
    return render(
        request,
        "registration/doctor_homepage.html",
        {"availabilities": availabilities}
    )

@login_required
def patient_homepage(request):
        doctors=DoctorProfileModel.objects.all()
        return render(
            request,"registration/patient_homepage.html",
            {"doctors":doctors}
        )

@login_required
def doctor_detail(request,id=id):
    doctor_detail=get_object_or_404(DoctorProfileModel,id=id)
    doctor_user=doctor_detail.user
    availability = AvailabilityModel.objects.filter(doctor_user=doctor_user)
    return render(request,"registration/doctor_detail.html",{"doctor_detail":doctor_detail,"availability":availability})


@login_required
def logout_view(request):
    logout(request)  # Ends the session
    return redirect("login")  # Redirect to login page (or homepage)
