from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Driver(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="driver")

    car_model = models.CharField(max_length=30,verbose_name="Модель авто")
    car_number = models.CharField(max_length=20,verbose_name="Номер машини")

    is_online  = models.BooleanField(default=False,verbose_name="Онлайн")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Курєр {self.user.username}"
