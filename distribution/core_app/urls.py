from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import (
    BaseStatusViewSet,
    RecaptchaTemplateView,
    # streaming_api,
    HistoryExportFileViewSet,
    TestingViewSet,
    RelatedModelViewSet,
    StatusViewSet,
)
from django.conf import settings

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(prefix="base-status", viewset=BaseStatusViewSet, basename="base-status")
router.register(
    prefix="history-export-files",
    viewset=HistoryExportFileViewSet,
    basename="history-export-files",
)
router.register(
    prefix="related-model-status",
    viewset=RelatedModelViewSet,
    basename="related-model-status",
)
router.register(prefix="status", viewset=StatusViewSet, basename="status")
router.register(prefix="testing", viewset=TestingViewSet, basename="testing")

urlpatterns = [
    path("", include(router.urls)),
    path("test", RecaptchaTemplateView.as_view(), name="recaptcha"),
]
