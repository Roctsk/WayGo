from django.urls import path
from .views import client_dashboard
from .views import check_order_status



urlpatterns = [
    path("dashboard/", client_dashboard, name="client-dashboard"),
    path("check-order-status/", check_order_status , name="check-order-status")
]