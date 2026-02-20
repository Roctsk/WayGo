from django.urls import path
from .views import rate_driver, rate_courier



urlpatterns = [
    path("rate-driver/<int:order_id>/",rate_driver , name="rate_driver"),
    path("rate-courier/<int:order_id>/", rate_courier, name="rate_courier"),
]
