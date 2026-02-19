from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import get_user_model, login
from .forms import CourierRegisterForm
from couriers.models import  Courier
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from orders.models import CourierOrder
from couriers.models import Courier
from django.conf import settings
from django.contrib import messages


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
        return render(request,"courier/actives_order.html",{"order":active_order,"courier":courier})

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
    return render(request,"couriers/courier_profile.html")


@login_required
def check_courier_status(request):
    order = CourierOrder.objects.filter(
        client=request.user,
        status__in=["accepted", "on_the_way", "completed"]
    ).last()

    if order:
        return JsonResponse({"status": order.status})
    return JsonResponse({"status": None})
