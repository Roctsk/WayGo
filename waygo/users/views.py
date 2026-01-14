from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from drivers.models import Driver
from couriers.models import Courier
from django.contrib.auth import login
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user.role == "driver":
                Driver.objects.create(user=user)
                redirect_url = "driver_dashboard"
            
            elif user.role == "courier":
                Courier.objects.create(user=user)
                redirect_url = "courier_dashboard"

            else:
                redirect_url = "home"

            login(request,user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request,"core/register.html",{"form":form})


@login_required
def role_redirect(request):
    user = request.user

    if user.role == "driver":
        return redirect("driver_dashboard")

    elif user.role == "courier":
        return redirect("courier_dashboard")

    return redirect("home")

