from django.shortcuts import render , redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

def home(request):
    return render(request,"core/home.html")


class CastomLoginView(LoginView):
    template_name = "core/login.html"

    def get_success_url(self):
        user = self.request.user

        if user.role == "client":
            return reverse_lazy("client_dashboard")
        elif user.role == "driver":
            return reverse_lazy("driver_dashboard")
        elif user.role == "courier":
            return reverse_lazy("courier_dashboard")
        
        return reverse_lazy("client_dashboard") 



