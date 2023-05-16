import io
from django.shortcuts import render
import polars
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, exceptions, viewsets, permissions, generics
from core_app.serializers import ExcelFileSerializer, StandardDataExcelFieldMultipleDetailSerializer

from core_app.views import BaseModelViewSet, RelatedQuerySetMixin
from .models import Order, OrderDetail, Purchase, PurchaseDetail
from .serializers import (ImportExcelOrderSerializer, OrderSerializer, OrderDetailSerializer, OrderDetailSerializerDetail,
                          OrderSerializerDetail, PurchaseSerializer, PurchaseDetailSerializer)
# Create your views here.
from django.db import transaction


class OrderCreationViewSet(BaseModelViewSet, RelatedQuerySetMixin):
    queryset = Order.objects.all()
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

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=["post"], detail=False, url_path="import-excel")
    def import_excel(self, request):
        file_serializer = StandardDataExcelFieldMultipleDetailSerializer(
            data=request.data, context={'request': request},
            model=self.model,
            detail_model=self.detail_model,
            add_exclude_fields=self.add_exclude_fields,
            add_validate_fields=self.add_validate_fields,
            field_detail_model_name=self.field_detail_model_name)
        file_serializer.is_valid(raise_exception=True)
        standard_data = file_serializer.save()
        count = 0
        position = 0
        error = []
        with transaction.atomic():
            for data in standard_data:
                serializer = self.import_serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                    count = count + 1
                else:
                    error.append({f"row {position}": serializer.errors})
                position = position + 1
        return Response(data={'message': "successfully", "data": {
            "success": f"{count} records",
            "failure": f"{len(error)} records",
            "error_description": error
        }}, status=status.HTTP_200_OK)
