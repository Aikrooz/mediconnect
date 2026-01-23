from django.shortcuts import render
from .models import AppointmentModel
from .forms import AppointmentForm
from account.models import DoctorProfileModel
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from .models import AppointmentModel, DoctorProfileModel
from .forms import AppointmentForm

def book_appointment(request, doctor_id):
    patient = request.user

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctor_detail = get_object_or_404(
                DoctorProfileModel, id=doctor_id
            )

            if form.cleaned_data.get("book") is True:
                AppointmentModel.objects.create(
                    doctor=doctor_detail,
                    patient=patient,
                    book=True,
                    message="You have an appointment",
                    read_message=False
                )

            return redirect("some-success-url")
    else:
        form = AppointmentForm()

    return render(request, "appointments/book.html", {"form": form})






