from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import BaseStatusViewSet
from django.conf import settings

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(prefix="base-status",
                viewset=BaseStatusViewSet, basename="base-status")

urlpatterns = [
    path('', include(router.urls)),
]
