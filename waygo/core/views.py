from django.shortcuts import render , redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse


def home(request):
    return render(request,"core/home.html")


class CastomLoginView(LoginView):
    template_name = "core/login.html"

    def get_success_url(self):
        user = self.request.user

        if user.role == "client":
            return redirect("client_dashboard")
        elif user.role == "driver":
            return redirect("driver_dashboard")
        elif user.role == "courier":
            return redirect("courier_dashboard")
        
        return reverse("client-dashboard")



