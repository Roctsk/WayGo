from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.courier_register , name="courier-register"),
    path("dashboard/",views.courier_dashboard , name="courier-dashboard"),
    path("toggle_onlines/",views.toggle_onlines , name="toggle-onlines"),
    path("courier_profile/", views.courier_profile, name="courier_profile"),
]
