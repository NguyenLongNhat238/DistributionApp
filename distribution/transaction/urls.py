from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import OrderCreationViewSet
from django.conf import settings

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(prefix="orders", viewset=OrderCreationViewSet,
                basename="orders")


urlpatterns = [
    path('', include(router.urls)),
]
