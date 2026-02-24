from django.contrib import admin
from .models import TaxiOrder , CourierOrder

admin.site.register(TaxiOrder)

admin.site.register(CourierOrder)
