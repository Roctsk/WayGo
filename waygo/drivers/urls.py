from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.driver_register , name="driver-register"),
    path("dashboard/",views.driver_dashboard , name="driver-dashboard"),
]
