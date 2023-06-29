from django.urls import path, include
from django.conf import settings
from rest_framework import routers

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

urlpatterns = [
    path("", include(router.urls)),
]
