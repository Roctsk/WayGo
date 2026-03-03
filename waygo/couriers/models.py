from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Courier(models.Model):

    TRANSPORT_CHOICE = (
        ("bike","Bike"),
        ("car","Car"),
        ("foot","On foot"),       
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="courier")

    transport = models.CharField(max_length=20,choices=TRANSPORT_CHOICE, verbose_name="Транспорт")
    is_online  = models.BooleanField(default=False,verbose_name="Онлайн")
    create_at = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    bonus_for_paid = models.PositiveIntegerField(default=0)
    rating_bonus_for_paid = models.PositiveIntegerField(default=0)
    ride_500_for_paid =  models.BooleanField(default=False)
    photo = models.ImageField(upload_to="courier_avatars//",blank=True,null=True)

    def __str__(self):
        return f"Курєр {self.user.phone}"



class CourierRating(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, related_name="ratings")
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.OneToOneField("orders.CourierOrder", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.courier.user.username} - {self.rating}⭐" 


