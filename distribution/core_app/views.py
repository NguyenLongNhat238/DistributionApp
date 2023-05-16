from rest_framework.decorators import action
from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from core_app.paginations import BasePagination

from core_app.permissions import BaseCompanyPermission
from core_app.serializers import ExcelFileSerializer
from .models import StatusBase


# Create your views here.


class BaseStatusViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        data = [{
            "name": StatusBase.STATUS_ACTIVE
        }, {
            "name": StatusBase.STATUS_INACTIVE
        }]
        return Response(data=data, status=status.HTTP_200_OK)


class RelatedQuerySetMixin:
    queryset = None
    select_related_fields = ()
    prefetch_related_fields = ()
    sort_fields = ()

    def get_related_queryset(self):
        queryset = self.queryset
        if len(self.select_related_fields) > 0:
            queryset = queryset.select_related(*self.select_related_fields)
        if len(self.prefetch_related_fields) > 0:
            queryset = queryset.prefetch_related(*self.select_related_fields)
        if len(self.sort_fields) > 0:
            queryset = queryset.order_by(*self.sort_fields)
        return queryset


class BaseModelViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView,
                       generics.CreateAPIView, generics.UpdateAPIView):
    pagination_class = BasePagination

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update', 'patch']:
            return [BaseCompanyPermission()]
        return [permissions.IsAuthenticated()]


class ActionImportExcelViewSet:
    import_serializer_class = None
    add_exclude_fields = ()
    add_validate_fields = ()
    model = None

    @action(methods=['post'], detail=False, url_path='import-excel')
    def import_excel(self, request):
        file_serializer = ExcelFileSerializer(data=request.data, context={
            'request': request},
            model=self.model,
            add_exclude_fields=self.add_exclude_fields,
            add_validate_fields=self.add_validate_fields)

        file_serializer.is_valid(raise_exception=True)
        data = file_serializer.save()

        count = 0
        position = 0
        error = []
        with transaction.atomic():
            for d in data:
                serializer = self.import_serializer_class(data=d)
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
