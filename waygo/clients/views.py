from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from drivers.models import Driver

@login_required
def client_dashboard(request):
    if request.user.role != "client":
        return redirect("home")
    
    online_drivers = Driver.objects.filter(is_online = True)
    
    return render(request,"clients/dashboard.html",  {"online_drivers":online_drivers})



