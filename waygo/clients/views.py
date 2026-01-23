from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from drivers.models import Driver
from orders.forms import TaxiOrderForm
from django.conf import settings
from django.contrib import messages
from drivers.views import calculate_price





@login_required
def client_dashboard(request):
    online_drivers = Driver.objects.filter(is_online = True)

    if request.method == "POST":
        form = TaxiOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user

            price = calculate_price(order.pickup_address, order.destination_address)
            if price is None:
                messages.error(request,"Не вдалося розрахувати маршрут. Перевірте адреси.")
                return redirect("client_dashboard")
            order.price = price

            order.save()
            messages.success(request, f"Замовлення створено! Орієнтовна ціна: {order.price} грн")
            return redirect("client_dashboard")
    else:
        form = TaxiOrderForm()
  
    
    return render(request,"clients/dashboard.html",  {"online_drivers":online_drivers, 'form':form,   "GOOGLE_API_KEY": settings.GOOGLE_MAPS_API_KEY})



