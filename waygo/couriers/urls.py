from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.courier_register , name="courier-register"),
    path("dashboard/",views.courier_register , name="courier-dashboard"),
]
