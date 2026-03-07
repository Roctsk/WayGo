from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import get_user_model, login
from .forms import CourierRegisterForm
from couriers.models import  Courier
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from orders.models import CourierOrder
from couriers.models import Courier , CourierRating
from django.conf import settings
from django.contrib import messages
from django.db.models import Avg
from .forms import CourierPhotoForm
from decimal import Decimal
from django.db.models import F
from datetime import timedelta
from django.utils import timezone


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
    if not hasattr(request.user, "courier"):
        return HttpResponseForbidden("Ви не є  кур'єром")
    
    courier = request.user.courier

    active_order = CourierOrder.objects.filter(
        courier=courier,
        status__in=["accepted", "on_the_way", "arrived"]
    ).first()

    if active_order:
        return render(request,"couriers/actives_order.html",{"order":active_order,"courier":courier})

    orders  = CourierOrder.objects.filter(
        status="created"
    )

    return render(request,"couriers/dashboard.html",{"orders":orders,"courier":courier})

@login_required
def curier_accept_order(request,order_id):
    courier = request.user.courier

    if CourierOrder.objects.filter(courier=courier,status__in=["accepted", "on_the_way", "arrived"]).exists():
        return HttpResponseForbidden("У вас вже є активне замовлення")

    order = get_object_or_404(
        CourierOrder, id=order_id,status="created")

    order.courier = courier
    order.status = "accepted"
    order.save()

    messages.success(request, "Замовлення прийнято!")
    return redirect("courier-dashboard")


@login_required
def courier_order_on_the_way(request):
    order = get_object_or_404(
        CourierOrder,
        courier=request.user.courier,
        status="accepted"
    )
    order.status = "on_the_way"
    order.save()
    return redirect("courier-dashboard")


@login_required
def courier_order_arrived(request):
    order = get_object_or_404(
        CourierOrder,
        courier=request.user.courier,
        status="on_the_way"
    )
    order.status = "arrived"
    order.save()
    return redirect("courier-dashboard")


@login_required
def courier_order_complete(request):
    order = get_object_or_404(
        CourierOrder,
        courier=request.user.courier,
        status="arrived"
    )
    order.status = "completed"
    order.save()
    courier = order.courier
    comletes_count = CourierOrder.objects.filter(courier=courier,status = "completed").count()

    earned_steps = comletes_count // 10
    new_steps = earned_steps - courier.bonus_for_paid
    if new_steps > 0:
        bonus_amount = Decimal("450.00") * new_steps
        Courier.objects.filter(pk = courier.pk).update(
            balance=F("balance") + bonus_amount,
            bonus_for_paid=F("bonus_for_paid") + new_steps,
        )
    
    return redirect("courier-dashboard")



@login_required
def courier_toggle_onlines(request):
    if request.method == "POST":
        courier = get_object_or_404(Courier, user=request.user)
        courier.is_online = not courier.is_online
        courier.save()
        return JsonResponse({"is_online": courier.is_online})
    return JsonResponse({"error": "POST request required"}, status=400)



def courier_profile(request):
    courier = request.user.courier
    completed_orders_qs = CourierOrder.objects.filter(courier=courier,status="completed")
    comleted_orders = completed_orders_qs.count()
    rating_avg = courier.ratings.aggregate(avg=Avg("rating"))["avg"] or 0

    now = timezone.localtime()
    start_of_day = now.replace(hour=0,minute=0,second=0,microsecond=0)
    start_of_week = start_of_day - timedelta(days=now.weekday())
    start_of_month = start_of_day.replace(day=1)
    start_of_year = start_of_day.replace(month=1,day=1)

    trip_starts = {
        "day": completed_orders_qs.filter(create_at__gte=start_of_day).count(),
        "week": completed_orders_qs.filter(create_at__gte=start_of_week).count(),
        "month": completed_orders_qs.filter(create_at__gte=start_of_month).count(),
        "year": completed_orders_qs.filter(create_at__gte=start_of_year).count(),
        "all_time": comleted_orders,
    }


    rated_orders = CourierRating.objects.filter(courier=courier).count()
    active_orders = CourierOrder.objects.filter(courier=courier, status__in = ["accepted","on_the_way"]).first()
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



    ride_goal = 500
    ride_reward = 5000
    ride_progress = min(comleted_orders ,ride_goal )
    ride_percent = int((ride_progress / ride_goal) *100 )
    ride_left = max(0, ride_goal - comleted_orders)

    context = {
        "courier":courier,
        "comleted_orders":comleted_orders,
        "active_orders":active_orders,
        "balance":courier.balance,
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
        "trip_starts": trip_starts ,

        "ride_goal": ride_goal,
        "ride_reward": ride_reward,
        "ride_progress": ride_progress,
        "ride_percent": ride_percent,
        "ride_left": ride_left,
        "rating_avg": round(rating_avg, 1),
    }
    return render(request,"couriers/couriers_profile.html",context)


@login_required
def check_courier_status(request):
    order = CourierOrder.objects.filter(
        client=request.user,
        status__in=["accepted", "on_the_way", "arrived", "completed"]
    ).order_by("-create_at").first()

    if order:
        return JsonResponse({"status": order.status})
    return JsonResponse({"status": None})



@login_required
def courier_upload_photo(request):
    courier = request.user.courier
    if request.method == "POST":
        form = CourierPhotoForm(request.POST, request.FILES , instance=courier)
        if form.is_valid():
            form.save()
    return redirect("courier_profile")





