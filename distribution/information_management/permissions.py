from rest_framework import permissions
from core_app.permissions import CompanyPermissionBase


class ManagerCompanyPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.user == obj.manager


class EmployeePermissions(CompanyPermissionBase):
    app_label = __module__.split(".")[0]
