from rest_framework import serializers

from core_app.serializers import BaseCompanyUserCreatedSerializer, CompanyModelBaseSerializer, ModelBaseSerializer, BaseModelUserCreatedSerializer
from user.serializers import UserBaseInformationSerializer
from .models import Company, Customer, Employee, Supplier


class CompanyBaseInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'detail']


class CompanySerializer(ModelBaseSerializer, BaseModelUserCreatedSerializer):
    class Meta:
        model = Company
        fields = ModelBaseSerializer.Meta.fields + BaseModelUserCreatedSerializer.Meta.fields + \
            ["name", "users", "detail", "manager"]
        read_only_fields = BaseModelUserCreatedSerializer.Meta.read_only_fields + \
            ['code', 'manager']
        extra_kwargs = {**ModelBaseSerializer.Meta.extra_kwargs,
                        **BaseModelUserCreatedSerializer.Meta.extra_kwargs}


class CompanyDetailSerializer(CompanySerializer):
    manager = UserBaseInformationSerializer()
    users = UserBaseInformationSerializer(many=True)

    class Meta:
        model = CompanySerializer.Meta.model
        fields = CompanySerializer.Meta.fields
        read_only_fields = CompanySerializer.Meta.read_only_fields
        extra_kwargs = {**CompanySerializer.Meta.extra_kwargs}


class CustomerSerializer(BaseCompanyUserCreatedSerializer):
    class Meta:
        model = Customer
        fields = BaseCompanyUserCreatedSerializer.Meta.fields + \
            ["first_name", "last_name", "shop_name", "full_address", "city",
                "district", "ward", "street", "house_number", "phone_number", "notes", "channel"]

        read_only_fields = BaseCompanyUserCreatedSerializer.Meta.read_only_fields
        extra_kwargs = {**BaseCompanyUserCreatedSerializer.Meta.extra_kwargs}


class CustomerDetailSerializer(CustomerSerializer):
    class Meta:
        model = CustomerSerializer.Meta.model
        fields = CustomerSerializer.Meta.fields + ["full_name"]
        read_only_fields = CustomerSerializer.Meta.read_only_fields + \
            ["full_name"]
        extra_kwargs = {**CustomerSerializer.Meta.extra_kwargs}


class EmployeeSerializer(BaseCompanyUserCreatedSerializer):
    class Meta:
        model = Employee
        fields = BaseCompanyUserCreatedSerializer.Meta.fields + \
            ["first_name", "last_name", "phone", "address"]

        read_only_fields = BaseCompanyUserCreatedSerializer.Meta.read_only_fields
        extra_kwargs = {**BaseCompanyUserCreatedSerializer.Meta.extra_kwargs}


class EmployeeDetailSerializer(EmployeeSerializer):
    class Meta:
        model = EmployeeSerializer.Meta.model
        fields = EmployeeSerializer.Meta.fields + ["full_name"]
        read_only_fields = EmployeeSerializer.Meta.read_only_fields + \
            ["full_name"]
        extra_kwargs = {**EmployeeSerializer.Meta.extra_kwargs}


class SupplierBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "code", "name"]


class SupplierSerializer(BaseCompanyUserCreatedSerializer):
    class Meta:
        model = Supplier
        fields = BaseCompanyUserCreatedSerializer.Meta.fields + \
            ["name", "address", "tax_code"]

        read_only_fields = BaseCompanyUserCreatedSerializer.Meta.read_only_fields
        extra_kwargs = {**BaseCompanyUserCreatedSerializer.Meta.extra_kwargs}


class SupplierDetailSerializer(SupplierSerializer):
    class Meta:
        model = SupplierSerializer.Meta.model
        fields = SupplierSerializer.Meta.fields
        read_only_fields = SupplierSerializer.Meta.read_only_fields
        extra_kwargs = {**SupplierSerializer.Meta.extra_kwargs}
