from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from drivers.models import Driver
from orders.forms import TaxiOrderForm
from django.conf import settings
from django.contrib import messages
from drivers.views import calculate_price
from orders.models import TaxiOrder





@login_required
def client_dashboard(request):
    online_drivers = Driver.objects.filter(is_online=True)
    active_order = TaxiOrder.objects.filter(
        client=request.user,
        status__in=["accepted", "in_progress"]
    ).first()
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

    return render(request, "clients/dashboard.html" , {"online_drivers":online_drivers,"active_order":active_order})

