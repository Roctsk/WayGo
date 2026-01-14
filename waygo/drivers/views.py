from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def driver_dashboard(request):
    if request.user.role != "driver":
        return render(request, "403.html")

    return render(request, "drivers/dashboard.html")# Create your views here.
