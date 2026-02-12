from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from drivers.models import Driver
from orders.forms import TaxiOrderForm
from django.conf import settings
from django.contrib import messages
from orders.models import TaxiOrder
from django.http import JsonResponse





@login_required
def client_dashboard(request):
    online_drivers = Driver.objects.filter(is_online=True)
    active_order = TaxiOrder.objects.filter(
        client=request.user
    ).order_by("-create_at").first()
    can_rate = False
    if active_order and active_order.status == "arrived":
        can_rate = not active_order.driver.ratings.filter(order=active_order).exists()
    if request.method == "POST":
        order = TaxiOrder.objects.create(
            client=request.user,
            pickup_address=request.POST["pickup_address"],
            destination_address=request.POST["destination_address"],
            comment = request.POST["comment"],
            city=request.POST["city"],
            status="searching"
        )
        return redirect("client-dashboard")

    return render(request, "clients/dashboard.html" , {"online_drivers":online_drivers,"active_order":active_order,"can_rate":can_rate})



@login_required
def check_order_status(request):
    order = TaxiOrder.objects.filter(
        client=request.user
    ).order_by("-create_at").first()

    if order:
        return JsonResponse({"status":order.status})
    return JsonResponse({"status":None})