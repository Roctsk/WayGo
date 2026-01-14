from django.urls import path
from .views import courier_dashboard


urlpatterns = [
    path("dashboard/", courier_dashboard, name="courier_dashboard")
]