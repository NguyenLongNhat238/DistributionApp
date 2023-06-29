from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import (
    DeliveryViewSet,
    DeliveryStatusViewSet,
    TransportViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(prefix="deliveries", viewset=DeliveryViewSet, basename="deliveries")

router.register(
    prefix="delivery-statuses",
    viewset=DeliveryStatusViewSet,
    basename="delivery-statuses",
)
router.register(prefix="transports", viewset=TransportViewSet, basename="transports")

urlpatterns = [
    path("", include(router.urls)),
]
