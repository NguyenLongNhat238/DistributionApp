from django.contrib import admin

from core_app.admin import BaseAdminSite
from .models import Order, OrderDetail, Purchase, PurchaseDetail

# Register your models here.


class OrderAdmin(BaseAdminSite):
    list_display = BaseAdminSite.list_display + ()
    list_select_related = BaseAdminSite.list_select_related + ()


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['id','order']

class PurchaseAdmin(BaseAdminSite):
    list_display = BaseAdminSite.list_display + ()
    list_select_related = BaseAdminSite.list_select_related = ()

class PurchaseDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)
admin.site.register(Purchase)
admin.site.register(PurchaseDetail)
