from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)

    is_client = models.BooleanField(default=True)
    is_driver = models.BooleanField(default=False)
    is_courier = models.BooleanField(default=False)

    def __str__(self):
        return self.phone
