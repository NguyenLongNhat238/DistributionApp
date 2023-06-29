from rest_framework import serializers
from .models import Order, OrderDetail, Purchase, PurchaseDetail
from core_app.serializers import (
    BaseCompanyUserCreatedSerializer,
    BaseModelUserCreatedSerializer,
    CompanyModelBaseSerializer,
    ValidateCodeCustomer,
    ValidateCodeEmployee,
    ValidateCodeProduct,
)
from django.db import transaction


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        # exclude = ['id']
        fields = "__all__"


class OrderSerializer(
    BaseCompanyUserCreatedSerializer, ValidateCodeCustomer, ValidateCodeEmployee
):
    order_details = OrderDetailSerializer(
        many=True, source="order_detail_order_related"
    )

    def create(self, validated_data):
        order_details_data = validated_data.pop("order_detail_order_related")
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for order_detail_data in order_details_data:
                OrderDetail.objects.create(order=order, **order_detail_data)
        return order

    class Meta:
        model = Order
        fields = BaseCompanyUserCreatedSerializer.Meta.fields + [
            "est_delivery_date",
            "order_date",
            "customer",
            "employee",
            "order_details",
        ]

        read_only_fields = BaseCompanyUserCreatedSerializer.Meta.read_only_fields
        extra_kwargs = {
            **BaseCompanyUserCreatedSerializer.Meta.extra_kwargs,
            # "order_details": {"write_only": True}
        }


class ImportExcelOrderDetailSerializer(OrderDetailSerializer, ValidateCodeProduct):
    def validate_product(self, value):
        product = super().validate_product(value)
        if product is None:
            raise serializers.ValidationError("This Code not exist!!")
        return product

    class Meta:
        model = OrderDetail
        # exclude = ['id']
        fields = "__all__"


class ImportExcelOrderSerializer(
    OrderSerializer, ValidateCodeCustomer, ValidateCodeEmployee
):
    order_details = ImportExcelOrderDetailSerializer(
        many=True, source="order_detail_order_related"
    )

    class Meta:
        model = Order
        fields = OrderSerializer.Meta.fields

        read_only_fields = OrderSerializer.Meta.read_only_fields
        extra_kwargs = {**OrderSerializer.Meta.extra_kwargs}


class OrderSerializerDetail(OrderSerializer):
    class Meta:
        model = OrderSerializer.Meta.model
        fields = OrderSerializer.Meta.fields
        read_only_fields = OrderSerializer.Meta.read_only_fields
        extra_kwargs = {**OrderSerializer.Meta.extra_kwargs}


class OrderDetailSerializerDetail(OrderDetailSerializer):
    class Meta:
        model = OrderDetailSerializer.Meta.model
        fields = OrderDetailSerializer.Meta.fields


class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        # exclude = ['id']
        fields = "__all__"


class ImportExcelPurchaseDetailSerializer(
    PurchaseDetailSerializer, ValidateCodeProduct
):
    def validate_product(self, value):
        product = super().validate_product(value)
        if product is None:
            raise serializers.ValidationError("This Code not exist!!")
        return product

    class Meta:
        model = PurchaseDetailSerializer.Meta.model
        # exclude = ['id']
        fields = "__all__"


class PurchaseSerializer(BaseCompanyUserCreatedSerializer):
    purchase_details = PurchaseDetailSerializer(
        many=True, source="purchase_detail_purchase_related"
    )

    class Meta:
        model = Purchase
        fields = BaseCompanyUserCreatedSerializer.Meta.fields + [
            "est_delivery_date",
            "purchase_date",
            "customer",
            "employee",
            "purchase_details",
        ]

        read_only_fields = BaseCompanyUserCreatedSerializer.Meta.read_only_fields
        extra_kwargs = {**BaseCompanyUserCreatedSerializer.Meta.extra_kwargs}


class PurchaseSerializerDetail(PurchaseSerializer):
    class Meta:
        model = PurchaseSerializer.Meta.model
        fields = PurchaseSerializer.Meta.fields
        read_only_fields = PurchaseSerializer.Meta.read_only_fields
        extra_kwargs = {**PurchaseSerializer.Meta.extra_kwargs}


class PurchaseDetailSerializerDetail(PurchaseDetailSerializer):
    class Meta:
        model = PurchaseDetailSerializer.Meta.model
        fields = PurchaseDetailSerializer.Meta.fields


class ImportExcelPurchaseSerializer(
    PurchaseSerializer, ValidateCodeCustomer, ValidateCodeEmployee
):
    purchase_details = ImportExcelPurchaseDetailSerializer(
        many=True, source="purchase_detail_purchase_related"
    )

    class Meta:
        model = PurchaseSerializer.Meta.model
        fields = PurchaseSerializer.Meta.fields

        read_only_fields = PurchaseSerializer.Meta.read_only_fields
        extra_kwargs = {**PurchaseSerializer.Meta.extra_kwargs}
