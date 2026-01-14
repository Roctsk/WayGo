from django.urls import path
from .views import register , role_redirect


urlpatterns = [
    path("register/",register,name="register"),
    path("redirect/", role_redirect, name="role_redirect"),
]