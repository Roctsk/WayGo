from django.shortcuts import render , redirect
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from .forms import DriverRegisterForm

User = get_user_model()

def driver_register(request):
    if request.method == "POST":
        form = DriverRegisterForm(request.POST)
        if form.is_valid():
            # беремо дані після валідації
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            phone = form.cleaned_data["phone"]

            # перевірка унікальності телефону
            if User.objects.filter(phone=phone).exists():
                form.add_error("phone", "Користувач з таким телефоном вже існує")
                return render(request, "drivers/register.html", {"form": form})

            # створюємо користувача
            user = User.objects.create_user(
                email=email,
                password=password,
                phone=phone
            )

            # створюємо водія
            driver = form.save(commit=False)
            driver.user = user
            driver.save()

            # логін
            login(request, user)
            return redirect("driver-dashboard")

    else:
        form = DriverRegisterForm()

    return render(request, "drivers/register.html", {"form": form})


def driver_dashboard(request):
    return render(request,"drivers/dashboard.html")


