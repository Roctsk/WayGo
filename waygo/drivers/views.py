from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from .forms import DriverRegisterForm
from .forms import DriverPhotoForm
from .models import Driver, DriverRating
from couriers.models import  Courier
from orders.models import TaxiOrder
from django.http import JsonResponse
from orders.models import  TaxiOrder
from django.http import HttpResponseForbidden
import requests
from django.conf import settings
from django.contrib import messages
from decimal import Decimal
from django.db.models import F


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
                username =username,
                role= "driver"
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

    active_order = TaxiOrder.objects.filter(
        driver=driver,
        status__in=["accepted", "on_the_way", "arrived"]
    ).first()

    if active_order:
        return render(request,"drivers/active_order.html",{"order":active_order,"driver":driver})

    orders  = TaxiOrder.objects.filter(
        status="searching",
        city__iexact=driver.city
    )

    return render(request,"drivers/dashboard.html",{"orders":orders,"driver":driver})





@login_required
def accept_order(request,order_id):
    driver = request.user.driver

    if TaxiOrder.objects.filter(driver=driver,status__in=["accepted", "on_the_way", "arrived"]).exists():
        return HttpResponseForbidden("У вас вже є активне замовлення")

    order = get_object_or_404(
        TaxiOrder, id=order_id,status="searching")

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
    


@login_required
def order_on_the_way(request):
    order = get_object_or_404(
        TaxiOrder,
        driver=request.user.driver,
        status="accepted"
    )
    order.status = "on_the_way"
    order.save()
    return redirect("driver-dashboard")


@login_required
def order_arrived(request):
    order = get_object_or_404(
        TaxiOrder,
        driver=request.user.driver,
        status="on_the_way"
    )
    order.status = "arrived"
    order.save()
    return redirect("driver-dashboard")


@login_required
def order_complete(request):
    order = get_object_or_404(
        TaxiOrder,
        driver=request.user.driver,
        status="arrived"
    )
    order.status = "completed"
    order.save()
    driver = order.driver
    comletes_count = TaxiOrder.objects.filter(driver=driver,status = "completed").count()

    earned_steps = comletes_count // 10
    new_steps = earned_steps - driver.bonus_for_paid
    if new_steps > 0:
        bonus_amount = Decimal("450.00") * new_steps
        Driver.objects.filter(pk = driver.pk).update(
            balance=F("balance") + bonus_amount,
            bonus_for_paid=F("bonus_for_paid") + new_steps,
        )


    return redirect("driver-dashboard")


def driver_profile(request):
    driver = request.user.driver
    comleted_orders = TaxiOrder.objects.filter(driver=driver,status="completed").count()
    rated_orders = DriverRating.objects.filter(driver=driver).count()
    active_orders = TaxiOrder.objects.filter(driver=driver, status__in = ["accepted","on_the_way"]).first()
    bonus_goal = 10
    bonus_reward = 450
    bonus_progress = comleted_orders % bonus_goal
    bonus_percent = int((bonus_progress / bonus_goal) *100 )
    bonus_left = bonus_goal - bonus_progress if bonus_progress else bonus_goal

    #Рейтинг бонус 
    rating_bonus_goal = 10
    rating_bonus_reward = 450
    rating_bonus_progress = rated_orders % rating_bonus_goal
    rating_bonus_percent = int((rating_bonus_progress / rating_bonus_goal) *100 )
    rating_bonus_left = rating_bonus_goal - rating_bonus_progress if rating_bonus_progress else rating_bonus_goal


    context = {
        "driver":driver,
        "comleted_orders":comleted_orders,
        "active_orders":active_orders,
        "balance":driver.balance,
        "bonus_goal": bonus_goal,
        "bonus_reward": bonus_reward,
        "bonus_progress": bonus_progress,
        "bonus_percent": bonus_percent,
        "bonus_left": bonus_left,

        "rated_orders": rated_orders,
        "rating_bonus_goal": rating_bonus_goal,
        "rating_bonus_reward": rating_bonus_reward,
        "rating_bonus_progress": rating_bonus_progress,
        "rating_bonus_percent": rating_bonus_percent,
        "rating_bonus_left": rating_bonus_left,
    }
    return render(request,"drivers/driver_profile.html",context)

@login_required
def driver_upload_photo(request):
    driver = request.user.driver
    if request.method == "POST":
        form = DriverPhotoForm(request.POST, request.FILES , instance=driver)
        if form.is_valid():
            form.save()
    return redirect("driver_profile")
