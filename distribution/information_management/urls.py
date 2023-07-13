from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import CompanyViewSet, EmployeeViewSet, SupplierViewSet, CustomerViewSet, ChannelViewSet
from django.conf import settings

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(prefix="companies", viewset=CompanyViewSet, basename="company")

router.register(prefix="customers", viewset=CustomerViewSet, basename="customers")

router.register(prefix="employees", viewset=EmployeeViewSet, basename="employees")

router.register(prefix="suppliers", viewset=SupplierViewSet, basename="suppliers")

router.register(prefix="channels", viewset=ChannelViewSet, basename="channels")

urlpatterns = [
    path("", include(router.urls)),
]
