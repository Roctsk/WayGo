from django.shortcuts import render , redirect
from django.contrib.auth import login
from users.forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)

            if user.role == "driver":
               return redirect("driver-register")

            elif user.role == "courier":
                return redirect("courier-register")

            return redirect("client-dashboard")

    else:
        form = RegisterForm()

    return render(request, "core/register.html", {"form": form})
