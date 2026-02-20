from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.courier_register , name="courier-register"),
    path("dashboard/",views.courier_dashboard , name="courier-dashboard"),
    path("toggle_onlines/",views.courier_toggle_onlines , name="courier-toggle-onlines"),
    path("accept_order/<int:order_id>/",views.curier_accept_order , name="courier_accept_order"),
    path("courier_profile/", views.courier_profile, name="courier_profile"),
    path("order/on-the-way/", views.courier_order_on_the_way, name="courier_order_on_the_way"),
    path("order/arrived/", views.courier_order_arrived, name="courier_order_arrived"),
    path("order/complete/", views.courier_order_complete, name="courier_order_complete"),
    path('check-courier-status/', views.check_courier_status, name='check-courier-status'),
    path("couriers_profile/", views.courier_profile, name="couriers_profile"),
]


