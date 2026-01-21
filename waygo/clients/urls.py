from django.urls import path
from .views import client_dashboard



urlpatterns = [
    path("dashboard/", client_dashboard, name="client-dashboard"),

]