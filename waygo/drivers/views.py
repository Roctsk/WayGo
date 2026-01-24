from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from .forms import DriverRegisterForm
from .models import Driver
from django.http import JsonResponse
from orders.models import  TaxiOrder
from django.http import HttpResponseForbidden
import requests
from django.conf import settings
from django.contrib import messages

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
            driver.city = form.cleaned_data['city']
            driver.save()

            login(request, user)
            return redirect("driver-dashboard")

    else:
        form = DriverRegisterForm()

    return render(request, "drivers/register.html", {"form": form})


def driver_dashboard(request):
    if not hasattr(request.user, "driver"):
        return HttpResponseForbidden("Ви не є водієм")
    
    driver = request.user.driver

    orders = TaxiOrder.objects.filter(
        status="searching",
        city__iexact=driver.city
    )

    return render(request,"drivers/dashboard.html",{"orders":orders,"driver":driver})



@login_required
def accept_order(request,order_id):
    driver = request.user.driver
    order = get_object_or_404(
        TaxiOrder, id=order_id,status="searching",pickup_address__icontains=driver.city)

    order.driver = driver
    order.status = "accepted"
    order.save()
    messages.success(request, "Замовлення прийнято!")
    return redirect("driver-dashboard")


@login_required
def toggle_online(request):
    if request.method == "POST":
        driver = get_object_or_404(Driver, user=request.user)
        driver.is_online = not driver.is_online
        driver.save()
        return JsonResponse({"is_online": driver.is_online})
    return JsonResponse({"error": "POST request required"}, status=400)



def calculate_price(pickup, destination):
    API_KEY = settings.GOOGLE_MAPS_API_KEY
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={pickup}&destination={destination}&key={API_KEY}"
    response = requests.get(url).json()

    if response['status'] == 'OK':
        distance_m = response['routes'][0]['legs'][0]['distance']['value']
        distance_km = distance_m / 1000
        base_fare = 50
        per_km = 10 
        return round(base_fare + per_km * distance_km, 2)
    else:
        return None
    