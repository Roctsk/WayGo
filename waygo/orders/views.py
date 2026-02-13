from django.shortcuts import render ,get_object_or_404 ,redirect
from django.contrib import messages
from .models import TaxiOrder
from drivers.models import DriverRating
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import JsonResponse

@login_required
def rate_driver(request,order_id):
    order = get_object_or_404(TaxiOrder , id=order_id, client=request.user)

    if order.status not in ["arrived", "completed"]:
        return JsonResponse({"error":"Не можна оцінити водія"}, status=400)

    
    if request.method == "POST":
        rating = int(request.POST.get("rating", 0))

        if rating < 1 or rating > 5:
            return JsonResponse({"error":"Оцінка від 1-"}, status=400)
        

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

        return JsonResponse({"success":True,"new_rating":driver.rating})

    return JsonResponse({"error":"POST required"}, status=400)


