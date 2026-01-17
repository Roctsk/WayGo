from django.shortcuts import render 
from django.contrib.auth.views import LoginView
from django.urls import reverse


def home(request):
    return render(request,"core/home.html")


def client_dashboard(request):
    return render(request,"clients/dashboard.html")



class CastomLoginView(LoginView):
    template_name = "core/login.html"

    def get_success_url(self):
        user = self.request.user

        if user.role == "driver":
            return reverse("driver-dashboard")
        if user.role == "courier":
            return reverse("courier-dashboard")
        
        return reverse("client-dashboard")



