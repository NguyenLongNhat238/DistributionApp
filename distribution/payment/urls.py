from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import OrderPaymentViewSet, PurchasePaymentViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(
    prefix="order-payments", viewset=OrderPaymentViewSet, basename="order-payments"
)
router.register(
    prefix="purchase-payments",
    viewset=PurchasePaymentViewSet,
    basename="purchase-payments",
)

urlpatterns = [
    path("", include(router.urls)),
]
