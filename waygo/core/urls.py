from django.urls import path
from .views import home
from  users.views import register
from . import views

urlpatterns = [
    path("",home, name="home"),
    path("register",register,name="register"),
    path("dashboard/", views.client_dashboard, name="client-dashboard"),
]