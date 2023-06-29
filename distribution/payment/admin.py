from django.contrib import admin
from .models import OrderPayment, PurchasePayment

# Register your models here.
admin.site.register(OrderPayment)
admin.site.register(PurchasePayment)
