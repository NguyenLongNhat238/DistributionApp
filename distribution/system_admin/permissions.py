from rest_framework import permissions
from .models import UserRole


class SystemAdminPermission(permissions.BasePermission):
    """
    Global permission check for system admin
    """

    def has_permission(self, request, view):
        method = request.method
        if request.user.is_company_manager():
            return True
        if request.user.is_system_admin():
            # Kiểm tra hành động
            if method in ["GET", "LIST"]:
                action = "View"
                permission = f"{action}_information_management"

            elif method == "POST":
                action = "Add"
                permission = f"{action}_information_management"

            elif method in ["PUT", "PATCH"]:
                action = "Change"
                permission = f"{action}_information_management"

            elif method == "DELETE":
                action = "Delete"
                permission = f"{action}_information_management"
            else:
                permission = "information_management"
            # Kiểm tra quyền
            if request.user.has_permissions(permission):
                return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if (
            request.user.is_company_manager() is True
            and obj.company == request.user.company is True
        ):
            return True
        return False
