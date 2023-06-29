from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions

from core_app.views import (
    BaseModelViewSet,
    BaseRelatedQueryViewSet,
    RelatedQuerySetMixin,
    ActionImportExcelViewSet,
    ActionExportExcelViewSet,
)
from .models import Order, OrderDetail, Purchase, PurchaseDetail
from .serializers import (
    ImportExcelOrderSerializer,
    ImportExcelPurchaseSerializer,
    OrderSerializer,
    OrderDetailSerializer,
    OrderDetailSerializerDetail,
    OrderSerializerDetail,
    PurchaseSerializer,
    PurchaseDetailSerializer,
)

# Create your views here.
from django.db import transaction


class OrderCreationViewSet(
    BaseModelViewSet,
    RelatedQuerySetMixin,
    ActionImportExcelViewSet,
    ActionExportExcelViewSet,
):
    queryset = Order.company_objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    select_related_fields = ()
    prefetch_related_fields = ()
    add_exclude_fields = ("order",)
    add_validate_fields = ()
    model = Order
    detail_model = OrderDetail
    field_detail_model_name = "order_details"
    import_serializer_class = ImportExcelOrderSerializer
    export_serializer = OrderSerializerDetail

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderDetailViewSet(BaseModelViewSet, RelatedQuerySetMixin):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    select_related_fields = ("product",)
    prefetch_related_fields = ()

    def get_queryset(self):
        query = self.get_related_queryset()
        return query


class PurchaseCreationViewSet(
    BaseRelatedQueryViewSet, ActionImportExcelViewSet, ActionExportExcelViewSet
):
    queryset = Order.company_objects.all()
    serializer_class = ImportExcelPurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    select_related_fields = BaseRelatedQueryViewSet.select_related_fields + ()
    prefetch_related_fields = BaseRelatedQueryViewSet.prefetch_related_fields + ()
    add_exclude_fields = ("order",)
    add_validate_fields = ()
    model = Purchase
    detail_model = PurchaseDetail
    field_detail_model_name = "perchase_details"
    import_serializer_class = ImportExcelOrderSerializer
    export_serializer = PurchaseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class PurchaseDetailViewSet(BaseModelViewSet, RelatedQuerySetMixin):
    queryset = PurchaseDetail.objects.all()
    serializer_class = PurchaseDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    select_related_fields = ("product",)
    prefetch_related_fields = ()

    def get_queryset(self):
        query = self.get_related_queryset()
        return query
