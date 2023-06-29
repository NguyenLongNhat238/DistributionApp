from django.http import StreamingHttpResponse, HttpResponse
from django.conf import settings
from django.views.generic import TemplateView
from rest_framework.decorators import action
from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, status, generics, permissions, exceptions
from rest_framework.response import Response
from core_app.paginations import BasePagination
from core_app.permissions import BaseCompanyPermission
from core_app.serializers import (
    ExcelFileSerializer,
    ExportedFileSerialzier,
    FileNameSerializer,
    StandardDataExcelFieldMultipleRowSerializer,
    StatusParameterSerializer,
    StatusSerializer,
)
from user.models import User
from .models import ExportedFile, Status, StatusBase
from .res_handing import ErrorHandling
import polars
from django.core.files.base import ContentFile
import tempfile
from datetime import datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# Create your views here.


class BaseStatusViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        data = [
            {"name": StatusBase.STATUS_ACTIVE},
            {"name": StatusBase.STATUS_INACTIVE},
        ]
        return Response(data=data, status=status.HTTP_200_OK)


class RelatedQuerySetMixin:
    queryset = None
    select_related_fields = ()
    prefetch_related_fields = ()
    sort_fields = ()

    def get_related_queryset(self):
        queryset = self.queryset
        if self.select_related_fields:
            queryset = queryset.select_related(*self.select_related_fields)
        if self.prefetch_related_fields:
            queryset = queryset.prefetch_related(*self.select_related_fields)
        if self.sort_fields:
            queryset = queryset.order_by(*self.sort_fields)
        return queryset


class BaseModelViewSet(
    viewsets.ViewSet,
    generics.ListAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
    generics.UpdateAPIView,
):
    pagination_class = BasePagination

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update", "patch"]:
            return [BaseCompanyPermission()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.model:
            return self.model.company_objects.all()
        return super().get_queryset()


class BaseRelatedQueryViewSet(BaseModelViewSet, RelatedQuerySetMixin):
    select_related_fields = ("company", "created_by", "updated_by")
    prefetch_related_fields = ()


class ActionImportExcelViewSet:
    import_serializer_class = None
    add_exclude_fields = ()
    add_validate_fields = ()
    model = None
    detail_model = None
    field_detail_model_name = None

    def get_file_excel(self):
        if self.detail_model:
            return StandardDataExcelFieldMultipleRowSerializer
        return ExcelFileSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["excel_file"],
            properties={
                "excel_file": openapi.Schema(type=openapi.TYPE_FILE),
            },
        ),
        responses={
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "success": openapi.Schema(type=openapi.TYPE_STRING),
                                "failure": openapi.Schema(type=openapi.TYPE_STRING),
                                "error_description": openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(type=openapi.TYPE_OBJECT),
                                ),
                            },
                        ),
                    },
                ),
            ),
        },
    )
    @action(methods=["post"], detail=False, url_path="import-excel")
    def import_excel(self, request):
        file_serializer = self.get_file_excel()
        file_serializer = file_serializer(
            data=request.data,
            context={"request": request},
            model=self.model,
            add_exclude_fields=self.add_exclude_fields,
            add_validate_fields=self.add_validate_fields,
            detail_model=self.detail_model,
            field_detail_model_name=self.field_detail_model_name,
        )

        file_serializer.is_valid(raise_exception=True)
        data = file_serializer.save()

        # count number records imported successfull
        count = 0
        # Position row of records in excel
        position = 1
        # List errors when import excel
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

        return Response(
            data={
                "message": "successfully",
                "data": {
                    "success": f"{count} records",
                    "failure": f"{len(error)} records",
                    "error_description": error,
                },
            },
            status=status.HTTP_200_OK,
        )


class ActionExportExcelViewSet:
    export_serializer = None
    queryset = None
    model_file = ExportedFile

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            # required=["file_name"],
            properties={"file_name": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        responses={
            200: openapi.Response(
                description="File download",
                content={
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
                        "schema": {"type": "string", "format": "binary"}
                    }
                },
                headers={
                    "Content-Disposition": openapi.Parameter(
                        "Content-Disposition",
                        openapi.IN_HEADER,
                        description="Attachment",
                        type=openapi.TYPE_STRING,
                    ),
                },
            ),
            # Add other possible response codes and descriptions here
        },
    )
    @action(methods=["post"], detail=False, url_path="export-excel")
    def export_excel(self, request):
        if self.get_queryset():
            query = self.get_queryset()
        else:
            raise exceptions.ValidationError(
                ErrorHandling(
                    message_en="Empty data.", message_vi="Dữ liệu rỗng.", code="DATA"
                ).to_representation()
            )
        file_name = request.data.get(
            "file_name", f"data_{self.queryset.model.__name__}"
        )
        serializer = self.export_serializer(
            query, many=True, context={"request": request}
        )
        data = serializer.data
        df = polars.DataFrame(data, infer_schema_length=1000)
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".xlsx") as temp_file:
            # Write the DataFrame to the temporary file
            df.write_excel(
                temp_file.name, worksheet="data", float_precision=2, autofit=True
            )
            # Read the content of the temporary file
            with open(temp_file.name, "rb") as file:
                content = file.read()
            # Create the ContentFile using the content
            content_file = ContentFile(content)
            # Create and save the ExportedFile
            exported_file = ExportedFile()
            exported_file.file.save(
                f"{file_name}_{datetime.now().timestamp()}.xlsx", content_file
            )
            exported_file.name_file = file_name
            exported_file.save()

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="{file_name}.xlsx"'
        response.write(content)
        return response


class HistoryExportFileViewSet(
    viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView
):
    queryset = ExportedFile.company_objects.all()
    serializer_class = ExportedFileSerialzier
    pagination_class = BasePagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = ExportedFile.company_objects.all()
        return queryset


class RelatedModelViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        choices = Status.RELATED_MODEL_CHOICES
        choices = [{"name": choice[0]} for choice in choices]
        return Response(data=choices, status=status.HTTP_200_OK)


class StatusViewSet(
    viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    queryset = Status.company_objects.all()
    serializer_class = StatusSerializer
    pagination_class = BasePagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Status.company_objects.all()
        params = self.request.query_params
        serialzier = StatusParameterSerializer(data=params)
        serialzier.is_valid(raise_exception=True)
        # queryset = queryset.filter(**serialzier.validated_data)
        queryset = queryset.filter(
            related_model=serialzier.validated_data["related_model"]
        )
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="related_model",
                required=True,
                in_=openapi.IN_QUERY,
                description="Related model status (required)",
                type=openapi.TYPE_STRING,
                enum=[choice[0] for choice in Status.RELATED_MODEL_CHOICES],
            ),
        ],
        query_serializer=StatusParameterSerializer,
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


def streaming_api(request):
    # Tạo generator để sinh ra dữ liệu dần dần
    if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        print("AAAAAAAAA")

    def data_generator():
        # Lấy dữ liệu từ nguồn nào đó, ví dụ: từ database, file, hoặc API khác
        data = 100 * "data"

        # Chia nhỏ dữ liệu thành các phần để trả về dần dần
        chunk_size = 1
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            yield chunk

            # Ngừng một khoảng thời gian trước khi gửi phần tiếp theo
            # Điều này giúp tạo ra dữ liệu dần dần, giống như streaming
            import time

            time.sleep(0.05)

    # Tạo phản hồi streaming response với generator dữ liệu
    response = StreamingHttpResponse(data_generator(), content_type="application/json")

    # Cấu hình header để cho phép streaming response
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"

    return response


class RecaptchaTemplateView(TemplateView):
    template_name = "test.html"

    def get(self, request, *args, **kwargs):
        template_name = self.get_template_names()
        import redis

        print(settings.CACHES)
        # Thực hiện kết nối tới Redis
        redis_host = "cache"
        redis_port = 6379
        redis_password = "JJk8iBHoFgLKtZ.zMQ!jz!T!@ozJ"  # Nếu có mật khẩu
        redis_client = redis.Redis(
            host=redis_host, port=redis_port, password=redis_password
        )

        # Ghi dữ liệu vào Redis
        redis_client.set("my_key", "my_value")

        # Đọc dữ liệu từ Redis
        value = redis_client.get("my_key")
        print(value)
        return render(request=request, template_name=template_name, context={})


# accounts/views.py
from django.shortcuts import render
from django.apps import apps
from django.contrib.auth.decorators import login_required


@login_required()
def new_user(request):
    users = User.objects.all()

    return render(request, "new_user.html", {"users": users})


class TestingViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        all_models = apps.get_models()

        model_names = [
            model.__name__
            for model in all_models
            if model._meta.app_config.name
            in [
                "delivery",
                "product",
                "information_management",
                "payment",
                "transaction",
            ]
        ]
        print(model_names)

        return Response(data={"message": "success"}, status=status.HTTP_200_OK)
