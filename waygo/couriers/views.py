from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def courier_dashboard(request):
    if request.user.role != "courier":
        return render(request, "403.html")

    return render(request, "couriers/dashboard.html")

