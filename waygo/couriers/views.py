from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import get_user_model, login
from .forms import CourierRegisterForm
from couriers.models import  Courier
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


User = get_user_model()

def courier_register(request):
    if request.method == "POST":
        form = CourierRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            phone = form.cleaned_data["phone"]
            username = form.cleaned_data["username"]

            # унікальності телефону
            if User.objects.filter(phone=phone).exists():
                form.add_error("phone", "Користувач з таким телефоном вже існує")
                return render(request, "couriers/register.html", {"form": form})

            # унікальності email
            if User.objects.filter(email=email).exists():
                form.add_error("email", "Користувач з таким email вже існує")
                return render(request, "couriers/register.html", {"form": form})

            user = User.objects.create_user(
                email=email,
                password=password,
                phone=phone,
                username =username,
                role = "courier"
            )

            courier = form.save(commit=False)
            courier.user = user
            courier.save()

            login(request, user)

            return redirect("courier-dashboard")
    else:
        form = CourierRegisterForm()

    return render(request, "couriers/register.html", {"form": form})

def courier_dashboard(request):
    return render(request,"couriers/dashboard.html")



@login_required
def toggle_onlines(request):
    if request.method == "POST":
        courier = get_object_or_404(Courier, user=request.user)
        courier.is_online = not courier.is_online
        courier.save()
        return JsonResponse({"is_online": courier.is_online})
    return JsonResponse({"error": "POST request required"}, status=400)



def courier_profile(request):
    return render(request,"couriers/courier_profile.html")
