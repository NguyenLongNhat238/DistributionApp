from rest_framework import serializers
from .models import Order, OrderDetail, Purchase, PurchaseDetail
from core_app.serializers import BaseModelUserCreatedSerializer, CompanyModelBaseSerializer, ValidateCodeCustomer, ValidateCodeEmployee, ValidateCodeProduct
from django.db import transaction


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        # exclude = ['id']
        fields = "__all__"


class OrderSerializer(CompanyModelBaseSerializer, BaseModelUserCreatedSerializer, ValidateCodeCustomer, ValidateCodeEmployee):
    order_details = OrderDetailSerializer(many=True,
                                          source="order_detail_order_related")

    def create(self, validated_data):
        order_details_data = validated_data.pop('order_detail_order_related')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for order_detail_data in order_details_data:
                OrderDetail.objects.create(order=order, **order_detail_data)
        return order

    class Meta:
        model = Order
        fields = CompanyModelBaseSerializer.Meta.fields + BaseModelUserCreatedSerializer.Meta.fields + \
            ["est_delivery_date", "order_date",
                "customer", "employee", "order_details", ]

        read_only_fields = BaseModelUserCreatedSerializer.Meta.read_only_fields + \
            CompanyModelBaseSerializer.Meta.read_only_fields
        extra_kwargs = {**CompanyModelBaseSerializer.Meta.extra_kwargs,
                        **BaseModelUserCreatedSerializer.Meta.extra_kwargs,
                        # "order_details": {"write_only": True}
                        }


class ImportExcelOrderDetailSerializer(OrderDetailSerializer, ValidateCodeProduct):

    class Meta:
        model = OrderDetail
        # exclude = ['id']
        fields = "__all__"


class ImportExcelOrderSerializer(OrderSerializer, ValidateCodeCustomer, ValidateCodeEmployee):
    order_details = ImportExcelOrderDetailSerializer(many=True,
                                                     source="order_detail_order_related")

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


class PurchaseSerializer(CompanyModelBaseSerializer, BaseModelUserCreatedSerializer):
    class Meta:
        model = Purchase
        fields = CompanyModelBaseSerializer.Meta.fields + BaseModelUserCreatedSerializer.Meta.fields + \
            ["date", "customer", "employee"]

        read_only_fields = BaseModelUserCreatedSerializer.Meta.read_only_fields + \
            CompanyModelBaseSerializer.Meta.read_only_fields
        extra_kwargs = {**CompanyModelBaseSerializer.Meta.extra_kwargs,
                        **BaseModelUserCreatedSerializer.Meta.extra_kwargs}


class PurchaseSerializerDetail(PurchaseSerializer):
    class Meta:
        model = PurchaseSerializer.Meta.model
        fields = PurchaseSerializer.Meta.fields
        read_only_fields = PurchaseSerializer.Meta.read_only_fields
        extra_kwargs = {**PurchaseSerializer.Meta.extra_kwargs}


class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        # exclude = ['id']
        fields = "__all__"


class PurchaseDetailSerializerDetail(PurchaseDetailSerializer):
    class Meta:
        model = PurchaseDetailSerializer.Meta.model
        fields = PurchaseDetailSerializer.Meta.fields
