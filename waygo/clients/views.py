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
    
    if request.method == "POST":
        order = TaxiOrder.objects.create(
            client=request.user,
            pickup_address=request.POST["pickup_address"],
            destination_address=request.POST["destination_address"],
            comment = request.POST["comment"],
            city=request.POST["city"],
            status="searching"
        )
        return redirect("client_dashboard")

    return render(request, "clients/dashboard.html" , {"online_drivers":online_drivers})

