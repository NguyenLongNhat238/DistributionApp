from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import PermissionViewSet, UserRoleViewSet, UserViewSet

from django.conf import settings

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(prefix="permissions", viewset=PermissionViewSet, basename="permissions")
router.register(prefix="user-roles", viewset=UserRoleViewSet, basename="user-roles")
router.register(
    prefix="users-management", viewset=UserViewSet, basename="users-management"
)
urlpatterns = [
    path("", include(router.urls)),
]
