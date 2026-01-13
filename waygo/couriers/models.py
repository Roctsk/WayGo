from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Courier(models.Model):

    TRANSPORT_CHOICE = (
        ("bike","Bike"),
        ("car","Car"),
        ("foot","On foot"),       
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="courier_profile")

    transport = models.CharField(max_length=20,choices=TRANSPORT_CHOICE, verbose_name="Транспорт")
    is_online  = models.BooleanField(default=False,verbose_name="Онлайн")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Курєр {self.user.phone}"

