from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import CompanyViewSet, EmployeeViewSet, SupplierViewSet, CustomerViewSet
from django.conf import settings

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(prefix="companies", viewset=CompanyViewSet, basename="company")

router.register(prefix="customers", viewset=CustomerViewSet, basename="customers")

router.register(prefix="employees", viewset=EmployeeViewSet, basename="employees")

router.register(prefix="supplier", viewset=SupplierViewSet, basename="supplier")


urlpatterns = [
    path("", include(router.urls)),
]
