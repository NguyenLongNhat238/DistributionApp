from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import InventoryViewSet, ProductViewSet, CategoryViewSet
from django.conf import settings

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(prefix="categories", viewset=CategoryViewSet,
                basename="categories")

router.register(prefix="products", viewset=ProductViewSet,
                basename="products")

router.register(prefix="inventories", viewset=InventoryViewSet,
                basename="Inventories")


urlpatterns = [
    path('', include(router.urls)),
]
