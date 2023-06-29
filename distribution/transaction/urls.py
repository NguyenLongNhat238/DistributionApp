from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import (
    OrderCreationViewSet,
    OrderDetailViewSet,
    PurchaseCreationViewSet,
    PurchaseDetailViewSet,
)
from django.conf import settings

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(prefix="orders", viewset=OrderCreationViewSet, basename="orders")

router.register(
    prefix="order-details", viewset=OrderDetailViewSet, basename="order-details"
)

router.register(
    prefix="purchases", viewset=PurchaseCreationViewSet, basename="purchases"
)

router.register(
    prefix="purchase-details",
    viewset=PurchaseDetailViewSet,
    basename="purchase-details",
)

urlpatterns = [
    path("", include(router.urls)),
]
