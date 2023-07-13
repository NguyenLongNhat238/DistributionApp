from rest_framework import permissions, exceptions
from django.apps import apps
from system_admin.models import UserRole


class BaseCompanyPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        Company = apps.get_model("information_management", "Company")
        company = Company.objects.filter(manager=request.user).first()
        return obj.company == company


class CompanyPermissionBase(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        # get request method
        method = request.method
        # get app_label from view
        app_label = view.__module__.split(".")[0]
        # get permission from request method
        if request.user.role:
            if (
                request.user.is_company_manager() is True
                or request.user.is_system_admin() is True
            ):
                return True
            if request.user.role.code == UserRole.ROLE_SYSTEM_EMPLOYEE:
                if method in ["GET", "LIST"]:
                    action = "View"
                    permission = f"{action}_{app_label}"

                elif method == "POST":
                    action = "Add"
                    permission = f"{action}_{app_label}"

                elif method in ["PUT", "PATCH"]:
                    action = "Change"
                    permission = f"{action}_{app_label}"

                elif method == "DELETE":
                    action = "Delete"
                    permission = f"{action}_{app_label}"
                else:
                    permission = app_label
                # Examine permission of user
                if request.user.has_permissions(permission):
                    return True

        return False

    def has_object_permission(self, request, view, obj):
        if (
            request.user.is_company_manager() is True
            or request.user.is_system_employee() is True
        ) and obj.company == request.user.company:
            return True
        return False
