from django.contrib import admin

from core_app.admin import BaseAdminSite
from .models import *

# Register your models here.


admin.site.site_header = "DISTRIBUTIONS"
admin.site.index_title = "Management Area"
admin.site.site_title = "Distributions"
admin.site.site_url = ""


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["code", "id", "name", "manager"]
    readonly_fields = [
        "created_at",
        "created_by",
        "code",
        "updated_at",
        "id",
        "updated_by",
        "slug",
    ]
    list_select_related = ("created_by", "manager", "updated_by")
    # fields = ['id', 'code', 'name', 'created_by', 'manager',
    #           'created_at', 'updated_at', 'status', 'updated_by']


class CustomerAdmin(BaseAdminSite):
    list_display = BaseAdminSite.list_display + ("shop_name", "company")
    list_select_related = BaseAdminSite.list_select_related


class EmployeeAdmin(BaseAdminSite):
    pass


class SupplierAdmin(BaseAdminSite):
    pass


admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Customer, CustomerAdmin)
