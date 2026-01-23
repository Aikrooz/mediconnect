from django.urls import path
from .views import create_user,create_doctor_profile,create_patient_profile,patient_homepage,doctor_homepage,login_view,doctor_detail,logout_view

urlpatterns=[
    path("create_user",create_user,name="create_user"),
    path("doctor_profile/",create_doctor_profile,name="doctor_profile"),
    path("patient_homepage/",patient_homepage,name="patient_homepage"),
    path("patient_profile/",create_patient_profile,name="patient_profile"),
    path("login",login_view,name="login"),
    path('logout/', logout_view, name='logout'),
    path("doctor_homepage",doctor_homepage,name="doctor_homepage"),
    path("doctor_detail/<int:id>",doctor_detail,name="doctor_detail")
]

# users should doctors should check set and edit availability.Also see what appointments they sent