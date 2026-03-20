from django.db import models
from django.conf import settings
from drivers.models import Driver
from couriers.models import Courier

class TaxiOrder(models.Model):

    STATUS_CHOICES = (
        ("searching", "Пошук водія"),
        ("accepted", "🚕 Водій прийняв замовлення"),
        ("on_the_way", "🚗 Водій їде до вас"),
        ("arrived", "📍 Водій на місці"),
        ("completed", "✅ Замовлення виконано"),
        ("cancelled", "Скасовано"),
    )

    client = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="taxi_orders")
    driver = models.ForeignKey(Driver,on_delete=models.SET_NULL,null=True,blank=True,related_name="orders")
    comment = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
    pickup_address = models.CharField(max_length=255)
    destination_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="searching")
    pickup_lat = models.FloatField(null=True, blank=True)
    pickup_lon = models.FloatField(null=True, blank=True)

    dest_lat = models.FloatField(null=True, blank=True)
    dest_lon = models.FloatField(null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Замовлення #{self.id} ({self.status})"



class CourierOrder(models.Model):

    STATUS_CHOICES = (
        ('created', 'Створено'),
        ('accepted', '📦 Курʼєр прийняв доставку'),
        ('on_the_way', '🚚 Курʼєр в дорозі'),
        ("arrived", "📍 Курʼєр на місці"),
        ('completed', "✅ Доставку завершено"),
    )

    client = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="courier_orders")
    courier = models.ForeignKey(Courier,on_delete=models.SET_NULL,null=True,blank=True,related_name="orders")
    comment = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
    pickup_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="created")

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Замовлення #{self.id} ({self.status})"