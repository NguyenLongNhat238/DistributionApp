from django.contrib import admin
from .models import *
# Register your models here.


admin.site.site_header = "DISTRIBUTIONS"
admin.site.index_title = "Management Area"
admin.site.site_title = "Distributions"
admin.site.site_url = ''


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['code', 'id', 'name', 'manager']
    readonly_fields = ['created_at', 'created_by',
                       'code', 'updated_at', 'id', 'updated_by', 'slug']
    # fields = ['id', 'code', 'name', 'created_by', 'manager',
    #           'created_at', 'updated_at', 'status', 'updated_by']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['code', 'id', 'shop_name', 'company']


admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee)
admin.site.register(Supplier)
admin.site.register(Customer, CustomerAdmin)
