from django.contrib.auth.forms import (
    UserChangeForm as DefaultUserChangeForm,
    UserCreationForm as DefaultUserCreationForm,
)
from django import forms
from .models import User,DoctorProfileModel,PatientProfileModel

#upadating the user details not the profiles
class UserChangeForm(DefaultUserChangeForm):

    class Meta:
        model = User
        fields = "__all__"

class UserCreationForm(DefaultUserCreationForm):
    class Meta:
        model = User
        fields = ["email","role",]



class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model=DoctorProfileModel
        fields="__all__"
        exclude=("user",)

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model=PatientProfileModel
        fields="__all__"
        exclude=("user",)
class LoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    
  
  
"""
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
"""