from django.urls import path
from .views import availability_view,edit_availability

urlpatterns=[
    path("available",availability_view,name="availability"),
    path("edit_availability/<int:id>",edit_availability,name="edit_availability")
]