from django.shortcuts import render ,get_object_or_404 ,redirect
from django.contrib import messages
from .models import TaxiOrder
from drivers.models import DriverRating
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

@login_required
def rate_driver(request,order_id):
    order = get_object_or_404(TaxiOrder , id=order_id, client=request.user)

    if order.status != "completed":
        messages.error(request ,"Ви можете оцінити водія лише після завершення поїздки." )
        return redirect("client-dashboard")
    
    if request.method == "POST":
        rating = int(request.POST.get("rating", 0))
        if rating < 1 or rating > 5:
            messages.error(request, "Оцінка повинна бути від 1 до 5.")
            return redirect("client-dashboard")
        

        DriverRating.objects.update_or_create(
            order=order,
            defaults={
                "driver": order.driver,
                "client": request.user,
                "rating": rating
            }
        )


        driver = order.driver
        avg = driver.ratings.aggregate(Avg("rating"))["rating__avg"]
        driver.rating = round(avg,1)
        driver.save()

        messages.success(request, f"Ви оцінили водія на {rating} ⭐")
        return redirect("driver-profile")

    return redirect("client-dashboard")

