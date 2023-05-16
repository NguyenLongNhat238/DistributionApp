from django.contrib import admin
from .models import Order, OrderDetail, Purchase, PurchaseDetail
# Register your models here.


admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Purchase)
admin.site.register(PurchaseDetail)
