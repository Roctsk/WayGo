from django.db import models
from waygo.users.models import User


class Courier(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    latitude = models.FloatField(null=True,blank=True)
    longitude  = models.FloatField(null=True,blank=True)

    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)

    VEHICLE_CHOICES = (
        ("car","Car"),
        ("bike","Bike"),
        ("scooter","Scooter"),
    )

    vehicle_type = models.CharField(max_length=20 ,choices=VEHICLE_CHOICES)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.vehicle_type})"