from rest_framework import permissions
from django.apps import apps
from system_admin.models import UserRole, Permission


class BaseCompanyPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        Company = apps.get_model("information_management", "Company")
        company = Company.objects.filter(manager=request.user).first()
        return obj.company == company


class CompanyPermissionBase(permissions.IsAuthenticated):
    app_label = __module__.split(".")[0]

    def has_permission(self, request, view):
        # Lấy hành động trong yêu cầu
        method = request.method
        app_label = self.app_label
        print("app_label", app_label)
        if request.user.role:
            if request.user.role.code == UserRole.ROLE_SYSTEM_ADDMIN:
                return True
            if request.user.role.code == UserRole.ROLE_SYSTEM_EMPLOYEE:
                # Kiểm tra hành động
                if method in ["GET", "LIST"]:
                    print("GET")
                    action = "View"
                    permission = f"{action}_{app_label}"

                elif method == "POST":
                    print("POST")
                    action = "Add"
                    permission = f"{action}_{app_label}"

                elif method in ["PUT", "PATCH"]:
                    print("PUT")
                    action = "Change"
                    permission = f"{action}_{app_label}"

                elif method == "DELETE":
                    print("DELETE")
                    action = "Delete"
                    permission = f"{action}_{app_label}"
                else:
                    permission = app_label
                # Kiểm tra quyền
                if request.user.has_permissions(permission):
                    print("has_permissions", permission)
                    return True

        return False

    def has_object_permission(self, request, view, obj):
        if (
            request.user.is_company_manager() is True
            or request.user.is_system_employee() is True
        ) and obj.company == request.user.company is True:
            return True
        return False
