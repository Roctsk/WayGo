from django.urls import path
from .views import rate_driver



urlpatterns = [
    path("rate-driver/<int:order_id>/",rate_driver , name="rate_driver"),
]