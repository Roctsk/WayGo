from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    ROLE_CHOICE = (
        ("client", "Client"),
        ("driver", "Driver"),
        ("courier", "Courier"),
    )
    REQUIRED_FIELDS = ["email", "phone"]

    phone = models.CharField(max_length=20, unique=True)

    role = models.CharField(max_length=30,choices=ROLE_CHOICE,default="client")


    def __str__(self):
        return self.phone
