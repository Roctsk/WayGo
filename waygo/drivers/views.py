from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from .forms import DriverRegisterForm
from .models import Driver
from django.http import JsonResponse

User = get_user_model()

def driver_register(request):
    if request.method == "POST":
        form = DriverRegisterForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            phone = form.cleaned_data["phone"]
            username = form.cleaned_data["username"]

             # унікальності телефону
            if User.objects.filter(phone=phone).exists():
                form.add_error("phone", "Користувач з таким телефоном вже існує")
                return render(request, "drivers/register.html", {"form": form})
            
             # унікальності email
            if User.objects.filter(email=email).exists():
                form.add_error("email", "Користувач з таким email вже існує")
                return render(request, "couriers/register.html", {"form": form})

            user = User.objects.create_user(
                email=email,
                password=password,
                phone=phone,
                username =username
            )

            driver = form.save(commit=False)
            driver.user = user
            driver.save()

            login(request, user)
            return redirect("driver-dashboard")

    else:
        form = DriverRegisterForm()

    return render(request, "drivers/register.html", {"form": form})


def driver_dashboard(request):
    driver = get_object_or_404(Driver, user=request.user)
    return render(request,"drivers/dashboard.html" , {"driver":driver})


@login_required
def toggle_online(request):
    if request.method == "POST":
        driver = get_object_or_404(Driver, user=request.user)
        driver.is_online = not driver.is_online
        driver.save()
        return JsonResponse({"is_online": driver.is_online})
    return JsonResponse({"error": "POST request required"}, status=400)