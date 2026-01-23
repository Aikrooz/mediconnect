from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .forms import AvailabilityForm,AvailabilityEditForm
from django.shortcuts import render,redirect   
from .models import AvailabilityModel
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def availability_view(request):
    doctor_profile = request.user# gets the current user
    if request.method == "POST":
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor_user = doctor_profile # The current user is attached to the docttor user field

            exists = AvailabilityModel.objects.filter(
                doctor_user=doctor_profile,
                day_of_week=availability.day_of_week,
                start_time=availability.start_time,
                end_time=availability.end_time,
            ).exists()

            if exists:
                form.add_error(None, "This availability already exists.")
            else:
                availability.full_clean() 
                availability.save()
                return redirect("doctor_homepage")   
    else:
        form = AvailabilityForm()

    return render(request, "availability.html", {"form": form})


@login_required
def edit_availability(request, id):
    doctor_profile = get_object_or_404(
        AvailabilityModel,
        id=id,
        doctor_user=request.user
    )

    if request.method == "POST":
        edit_form = AvailabilityEditForm(
            instance=doctor_profile,
            data=request.POST
        )
        if edit_form.is_valid():
            edit_form.save()
            return redirect("availability")
    else:
        edit_form = AvailabilityEditForm(instance=doctor_profile)

    return render(
        request,
        "edit_availability.html",
        {"edit_form": edit_form}
    )
