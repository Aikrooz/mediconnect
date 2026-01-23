from django import forms 
from django.core.exceptions import ValidationError
from .models import AvailabilityModel

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model=AvailabilityModel
        fields=("day_of_week","start_time","end_time")
        widgets={
            "days_of_week":forms.Select(),
            "end_time":forms.TimeInput(attrs={"type":"time"}),
            "start_time":forms.TimeInput(attrs={"type":"time"})
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time:
            if start_time >= end_time:
                raise ValidationError(
                    "End time must be greater than start time."
                )

        return cleaned_data

class AvailabilityEditForm(forms.ModelForm):
    class Meta:
        model = AvailabilityModel
        fields = ["day_of_week", "start_time", "end_time"]
        widgets={
            "days_of_week":forms.Select(),
            "end_time":forms.TimeInput(attrs={"type":"time"}),
            "start_time":forms.TimeInput(attrs={"type":"time"})
        }
