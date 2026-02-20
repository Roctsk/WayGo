from django.shortcuts import render ,get_object_or_404 ,redirect
from django.contrib import messages
from .models import TaxiOrder, CourierOrder
from drivers.models import DriverRating
from couriers.models import CourierRating
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


@login_required
def rate_courier(request, order_id):
    order = get_object_or_404(CourierOrder, id=order_id, client=request.user)

    if order.status not in ["arrived", "completed"]:
        return JsonResponse({"error": "Не можна оцінити кур'єра"}, status=400)

    if request.method == "POST":
        rating = int(request.POST.get("rating", 0))

        if rating < 1 or rating > 5:
            return JsonResponse({"error": "Оцінка від 1 до 5"}, status=400)

        if not order.courier:
            return JsonResponse({"error": "Кур'єр не призначений"}, status=400)

        CourierRating.objects.update_or_create(
            order=order,
            defaults={
                "courier": order.courier,
                "client": request.user,
                "rating": rating,
            },
        )

        courier = order.courier
        avg = courier.ratings.aggregate(Avg("rating"))["rating__avg"]

        return JsonResponse({"success": True, "new_rating": round(avg, 1) if avg else 0})

    return JsonResponse({"error": "POST required"}, status=400)


