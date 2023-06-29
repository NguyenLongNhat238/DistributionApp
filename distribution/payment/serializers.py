from rest_framework import serializers
from .models import OrderPayment, PurchasePayment
from core_app.serializers import BaseCompanyUserCreatedSerializer


class OrderPaymentSerializer(BaseCompanyUserCreatedSerializer):
    class Meta:
        model = OrderPayment
        fields = BaseCompanyUserCreatedSerializer.Meta.fields + [
            "payment_status",
            "order",
            "payment_date",
            "paid_amount",
            "excess_amount",
            "remaining_amount",
        ]
        read_only_fields = BaseCompanyUserCreatedSerializer.Meta.read_only_fields
        extra_kwargs = {**BaseCompanyUserCreatedSerializer.Meta.extra_kwargs}


class OrderPaymentDetailSerialzier(OrderPaymentSerializer):
    class Meta:
        model = OrderPayment
        fields = OrderPaymentSerializer.Meta.fields + [
            "paid_amount_currency",
            "excess_amount_currency",
            "remaining_amount_currency",
        ]
        read_only_fields = OrderPaymentSerializer.Meta.read_only_fields
        extra_kwargs = {**OrderPaymentSerializer.Meta.extra_kwargs}


class PurchasePaymentSerializer(BaseCompanyUserCreatedSerializer):
    class Meta:
        model = PurchasePayment
        fields = BaseCompanyUserCreatedSerializer.Meta.fields + [
            "payment_status",
            "purchase",
            "payment_date",
            "paid_amount",
            "excess_amount",
            "remaining_amount",
        ]
        read_only_fields = BaseCompanyUserCreatedSerializer.Meta.read_only_fields
        extra_kwargs = {**BaseCompanyUserCreatedSerializer.Meta.extra_kwargs}


class PurchasePaymentDetailSerialzier(PurchasePaymentSerializer):
    class Meta:
        model = PurchasePayment
        fields = PurchasePaymentSerializer.Meta.fields + [
            "paid_amount_currency",
            "excess_amount_currency",
            "remaining_amount_currency",
        ]
        read_only_fields = PurchasePaymentSerializer.Meta.read_only_fields
        extra_kwargs = {**PurchasePaymentSerializer.Meta.extra_kwargs}
