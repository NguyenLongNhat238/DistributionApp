from rest_framework import permissions
from django.apps import apps


class BaseCompanyPermission(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        Company = apps.get_model(
            'information_management', 'Company')
        company = Company.objects.filter(
            manager=request.user).first()
        return obj.company == company
