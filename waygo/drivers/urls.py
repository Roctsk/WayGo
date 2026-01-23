from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.driver_register , name="driver-register"),
    path("dashboard/",views.driver_dashboard , name="driver-dashboard"),
    path("toggle_online/",views.toggle_online , name="toggle-online"),
    path("accept_order/<int:order_id>/",views.accept_order , name="accept_order"),
]
