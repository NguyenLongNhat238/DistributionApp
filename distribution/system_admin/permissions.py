from rest_framework import permissions
from .models import UserRole


class SystemAdminPermission(permissions.BasePermission):
    """
    Global permission check for system admin
    """

    def has_permission(self, request, view):
        method = request.method
        print(request.user.is_company_manager(), request.user.is_authenticated)
        if request.user.is_authenticated is True:
            if request.user.is_company_manager() is True:
                return True
            if request.user.is_system_admin():
                # Kiểm tra hành động
                if method in ["GET", "LIST"]:
                    action = "View"
                    permission = f"{action}_user"

                elif method == "POST":
                    action = "Add"
                    permission = f"{action}_user"

                elif method in ["PUT", "PATCH"]:
                    action = "Change"
                    permission = f"{action}_user"

                elif method == "DELETE":
                    action = "Delete"
                    permission = f"{action}_user"
                else:
                    permission = "user"
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
            and obj.company == request.user.company
        ):
            return True
        return False
