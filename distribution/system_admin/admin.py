from django.contrib import admin
from django.http.request import HttpRequest
from .models import UserRole, Permission

# Register your models here.


class PermissionAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    list_filter = ["name", "code"]
    search_fields = ["name", "code"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    list_filter = ["name", "code"]
    search_fields = ["name", "code"]


admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(Permission, PermissionAdmin)
