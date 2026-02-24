from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from drivers.models import Driver
from couriers.models import Courier
from orders.models import TaxiOrder, CourierOrder
from django.http import JsonResponse
from django.db.models import Avg





@login_required
def client_dashboard(request):
    online_drivers = Driver.objects.filter(is_online=True)
    online_couriers = Courier.objects.filter(is_online=True).annotate(rating_avg=Avg("ratings__rating"))

    active_taxi_order = TaxiOrder.objects.filter(
        client=request.user
    ).order_by("-create_at").first()

    active_courier_order = CourierOrder.objects.filter(
        client=request.user
    ).order_by("-create_at").first()

    can_rate_driver = False
    if (
        active_taxi_order
        and active_taxi_order.driver
        and active_taxi_order.status in ["arrived", "completed"]
    ):
        can_rate_driver = not active_taxi_order.driver.ratings.filter(order=active_taxi_order).exists()

    can_rate_courier = False
    if (
        active_courier_order
        and active_courier_order.courier
        and active_courier_order.status in ["arrived", "completed"]
    ):
        can_rate_courier = not active_courier_order.courier.ratings.filter(order=active_courier_order).exists()
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "taxi":
            TaxiOrder.objects.create(
                client=request.user,
                pickup_address=request.POST["pickup_address"],
                destination_address=request.POST["destination_address"],
                comment=request.POST.get("comment"),
                city=request.POST["city"],
                status="searching"
            )
        elif form_type == "courier":
            CourierOrder.objects.create(
                client=request.user,
                pickup_address=request.POST["pickup_address"],
                delivery_address=request.POST["delivery_address"],
                comment=request.POST.get("comment"),
                status="created"
            )
        return redirect("client-dashboard")

    return render(
        request,
        "clients/dashboard.html",
        {
            "online_drivers": online_drivers,
            "online_couriers": online_couriers,
            "active_taxi_order": active_taxi_order,
            "active_courier_order": active_courier_order,
            "can_rate_driver": can_rate_driver,
            "can_rate_courier": can_rate_courier,
        },
    )



@login_required
def check_order_status(request):
    order = TaxiOrder.objects.filter(
        client=request.user
    ).order_by("-create_at").first()

    if order:
        return JsonResponse({"status":order.status})
    return JsonResponse({"status":None})



def client_profile(request):
    return render(request,"clients/client_profile.html")