from django.urls import path
from . import views

app_name = 'booking'  # This allows you to use namespaced URLs like 'booking:book_appointment'

urlpatterns = [
    # Public/Home page
    path('', views.index, name='index'),
    
    # Booking flow
    path('book/', views.book_appointment, name='book_appointment'),
    path('book/time/', views.select_time, name='select_time'),
    
    # User appointment management
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('appointment/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    
    # Staff/Admin management
    path('staff/appointments/', views.manage_appointments, name='manage_appointments'),
    path('staff/appointment/<int:appointment_id>/update-status/', views.update_appointment_status, name='update_appointment_status'),
    
    # Optional: Doctor management (if you want public doctor listing)
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
]