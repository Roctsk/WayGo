from django.urls import path
from .views import home
from  users.views import register
from .views import CastomLoginView
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("",home, name="home"),
    path("register",register,name="register"),
    path("dashboard/", views.client_dashboard, name="client-dashboard"),
    path("login/",CastomLoginView.as_view(),name="login"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
]