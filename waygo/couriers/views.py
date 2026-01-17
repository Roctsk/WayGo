from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from .forms import CourierRegisterForm

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
                username =username
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
