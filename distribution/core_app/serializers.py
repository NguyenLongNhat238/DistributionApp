import io
import os
import polars
from rest_framework import serializers, exceptions
from django.core import exceptions as core_exceptions
from core_app.get_username import get_request
from core_app.models import ExportedFile, History, ModelBase, CompanyModelBase, Status
from information_management.models import Customer, Employee, Supplier
from product.models import Category, MeasurementUnit, Product
from transaction.models import Order
from user.serializers import UserBaseInformationSerializer
from collections import Counter


class ModelBaseSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        model = ModelBase
        fields = [
            "id",
            "code",
            "status",
            "created_at",
            "updated_at",
            "slug",
        ]
        read_only_fields = ["slug"]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)


class CompanyModelBaseSerializer(ModelBaseSerializer):
    # company_detail = serializers.SerializerMethodField(read_only=True)

    def validate_code(self, value):
        company = self.initial_data.get("company", None)
        model = self.Meta.model
        if company is None:
            exist_code_company = model.company_objects.filter(code=value)
            if exist_code_company:
                raise serializers.ValidationError(
                    f"Duplicate {model._meta.model_name} code for the company."
                )

        return value

    def get_company_detail(self, obj):
        return "Company detail"

    class Meta:
        abstract = True
        model = CompanyModelBase
        read_only_fields = ModelBaseSerializer.Meta.read_only_fields + ["company"]
        fields = ModelBaseSerializer.Meta.fields + ["company"]
        extra_kwargs = {**ModelBaseSerializer.Meta.extra_kwargs}


class BaseModelUserCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        model = ModelBase
        fields = ["created_by", "updated_by"]
        read_only_fields = ["created_by", "updated_by"]
        extra_kwargs = {}


class BaseCompanyUserCreatedSerializer(
    CompanyModelBaseSerializer, BaseModelUserCreatedSerializer
):
    class Meta:
        abstract = True
        model = CompanyModelBase
        fields = (
            CompanyModelBaseSerializer.Meta.fields
            + BaseModelUserCreatedSerializer.Meta.fields
        )

        read_only_fields = (
            BaseModelUserCreatedSerializer.Meta.read_only_fields
            + CompanyModelBaseSerializer.Meta.read_only_fields
        )

        extra_kwargs = {
            **CompanyModelBaseSerializer.Meta.extra_kwargs,
            **BaseModelUserCreatedSerializer.Meta.extra_kwargs,
        }


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "name", "description", "related_model", "created_at"]
        extra_kwargs = {"related_model": {"write_only": True}}


class StatusParameterSerializer(serializers.Serializer):
    related_model = serializers.ChoiceField(
        choices=Status.RELATED_MODEL_CHOICES, required=True
    )


class FileNameSerializer(serializers.Serializer):
    file_name = serializers.CharField(max_length=255)


class ExcelFileSerializer(serializers.Serializer):
    data_import = serializers.ListField(required=False)

    excel_file = serializers.FileField(required=True)
    exclude_fields = [
        "id",
        "status",
        "slug",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "company",
    ]
    add_exclude_fields = ()
    add_validate_fields = ()

    all_exclude_field_names = ()
    all_validate_field_names = ()

    model = None
    detail_model = None
    field_detail_model_name = "detail"

    # Set all exclude field names to self.all_exclude_field_names: base + add fields
    def set_all_exclude_field_names(self):
        exclude_field_name = self.exclude_fields
        if self.add_exclude_fields:
            exclude_field_name = [*self.add_exclude_fields, *self.exclude_fields]
        self.all_exclude_field_names = exclude_field_name
        print("exclude - ", exclude_field_name)

    # Set all validate fields names to self.all_validate_field_names: model + add_validate + model detail
    def set_all_validate_field_names(self):
        if self.detail_model:
            validate_field_names = [
                *[f.name for f in self.model._meta.get_fields()],
                *[f.name for f in self.detail_model._meta.get_fields()],
            ]
        else:
            validate_field_names = [f.name for f in self.model._meta.get_fields()]
        if self.add_validate_fields:
            validate_field_names.extend(self.add_validate_fields)
        self.all_validate_field_names = validate_field_names
        print(validate_field_names)

    # validate just upload excel in field excel_file
    def validate_excel_file(self, value):
        ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
        valid_extensions = [".xlsx", ".xls", ".csv"]
        if ext.lower() not in valid_extensions:
            raise serializers.ValidationError(
                {"excel_file": "Unsupported file extension."}
            )
        return value

    def validate(self, attrs):
        model = self.model
        errors = {}
        # file = self.context.get("request").FILES['excel_file']
        file = attrs["excel_file"]
        data = io.BytesIO(file.read())
        df = polars.read_excel(
            data,
            sheet_id=1,
            read_csv_options={
                "has_header": True,
                "infer_schema_length": 1000,
                "ignore_errors": True,
            },
        )
        df.columns = list(map(lambda x: str.lower(x.split("(")[0]), df.columns))
        est_validate_fields = []
        # Check field validate
        if model:
            self.set_all_exclude_field_names()
            self.set_all_validate_field_names()
            for f in self.all_validate_field_names:
                if (
                    f not in self.all_exclude_field_names
                    and not f.endswith("related")
                    and not f.endswith("currency")
                ):
                    # Store actual validate fields
                    est_validate_fields.append(str.upper(f))
                    # Store fields have not in excel file
                    if f not in df.columns:
                        errors.update({str.upper(f): "This field required in excel!"})
        else:
            raise serializers.ValidationError(
                {"message": "You are not declare MODEL for import!"}
            )
        if errors:
            raise serializers.ValidationError(
                {"message": errors, "fields": est_validate_fields}
            )
        self.data_import = df.to_dicts()
        return super().validate(attrs)

    def save(self, **kwargs):
        return self.data_import

    def __init__(self, *args, **kwargs):
        self.add_exclude_fields = kwargs.pop("add_exclude_fields", None)
        self.add_validate_fields = kwargs.pop("add_validate_fields", None)
        self.all_validate_field_names = kwargs.pop("all_validate_field_names", None)
        self.all_exclude_field_names = kwargs.pop("all_exclude_field_names", None)
        self.model = kwargs.pop("model", None)
        self.detail_model = kwargs.pop("detail_model", None)
        self.field_detail_model_name = kwargs.pop("field_detail_model_name", None)
        super().__init__(*args, **kwargs)


class StandardDataExcelFieldMultipleRowSerializer(ExcelFileSerializer):
    def standard_data(self, data, field_names):
        # Group data
        grouped_data = {}
        for item in data:
            code = item.get("code")
            if code is not None:
                if code in grouped_data:
                    grouped_data[code].append(item)
                else:
                    grouped_data[code] = [item]
        # Standard data
        standard_data = []
        for item in grouped_data.keys():
            detail = []
            main = {}
            for i in grouped_data[item]:
                for f in field_names:
                    if (
                        f not in self.all_exclude_field_names
                        and not f.endswith("related")
                        and not f.endswith("currency")
                    ):
                        main[f] = i.pop(f)
                detail.append(i)
            main[f"{self.field_detail_model_name}"] = detail
            standard_data.append(main)
        return standard_data

    def validate(self, attrs):
        super().validate(attrs)
        dict_data = self.data_import
        fields = self.model._meta.get_fields()
        self.data_import = self.standard_data(
            data=dict_data, field_names=[f.name for f in fields]
        )
        return attrs


class ValidateCodeCustomer(serializers.Serializer):
    customer = serializers.CharField()

    def validate_customer(self, value):
        if value:
            cus = Customer.company_objects.filter(code=value).first()
            if cus:
                return cus
            else:
                return Customer.objects.create(code=value)
        return None


class ValidateCodeEmployee(serializers.Serializer):
    employee = serializers.CharField()

    def validate_employee(self, value):
        if value:
            employee = Employee.company_objects.filter(code=value).first()
            if employee:
                return employee
            else:
                return Employee.objects.create(code=value)
        return None


class ValidateCodeProduct(serializers.Serializer):
    product = serializers.CharField()

    def validate_product(self, value):
        if value:
            product = Product.company_objects.filter(code=value).first()
            if product:
                return product
        return None


class ValidateCodeSupplier(serializers.Serializer):
    supplier = serializers.CharField()

    def validate_supplier(self, value):
        if value:
            supplier = Supplier.company_objects.filter(code=value).first()
            if supplier:
                return supplier
            else:
                return Supplier.objects.create(code=value)
        return None


class ValidateCodeOrder(serializers.Serializer):
    order = serializers.CharField()

    def validate_order(self, value):
        if value:
            order = Order.company_objects.filter(code=value).first()
            if order:
                return Order.objects.create(code=value)
        return None


class ValidateCodeCategory(serializers.Serializer):
    category = serializers.CharField()

    def validate_order(self, value):
        if value:
            category = Category.company_objects.filter(code=value).first()
            if category:
                return category
            else:
                return Category.objects.create(code=value)
        return None


class ValidateMeasurementUnitName(serializers.Serializer):
    unit = serializers.CharField()

    def validate_unit(self, value):
        if value:
            unit = MeasurementUnit.company_objects.filter(name=value).first()
            if unit:
                return unit
            else:
                return MeasurementUnit.objects.create(name=value)
        return None


class ExportedFileSerialzier(BaseCompanyUserCreatedSerializer):
    file_name = serializers.SerializerMethodField(read_only=True)
    file_path = serializers.SerializerMethodField(read_only=True)

    def get_file_name(self, obj):
        return obj.file.name

    def get_file_path(self, obj):
        return obj.file.path

    class Meta:
        model = ExportedFile
        fields = BaseCompanyUserCreatedSerializer.Meta.fields + [
            "file",
            "file_name",
            "file_path",
        ]

        read_only_fields = BaseCompanyUserCreatedSerializer.Meta.read_only_fields
        extra_kwargs = {
            **BaseCompanyUserCreatedSerializer.Meta.extra_kwargs,
        }


class HistorySerialzier(serializers.ModelSerializer):
    class Meta:
        read_only = True
        model = History
        fields = ['id','action', 'model_name', 'object_id', 'data', 'user']