from django.contrib import admin
from .models import Product, Category, Inventory, Warehouse, MeasurementUnit
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_purchase_price', 'id')

    def formatted_purchase_price(self, obj):
        return obj.purchase_price.__str__()


admin.site.register(MeasurementUnit)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Inventory)
admin.site.register(Warehouse)
