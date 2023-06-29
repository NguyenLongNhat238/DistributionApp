from rest_framework import serializers
from .models import Delivery, DeliveryStatus, Transport
from core_app.serializers import BaseCompanyUserCreatedSerializer


class DeliverySerializer(BaseCompanyUserCreatedSerializer):
    class Meta:
        model = Delivery
        fields = BaseCompanyUserCreatedSerializer.Meta.fields + [
            "delivery_status",
            "shipper",
            "order",
            "delivery_date",
        ]
        read_only_fields = BaseCompanyUserCreatedSerializer.Meta.read_only_fields
        extra_kwargs = {**BaseCompanyUserCreatedSerializer.Meta.extra_kwargs}


class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = [
            "id",
            "status",
            "delivery",
            "note",
            "date",
        ]
        read_only_fields = ["id", "date"]


class DeliveryStatusParamSerializer(serializers.Serializer):
    delivery_id = serializers.IntegerField(required=True)


class TransportSerializer(BaseCompanyUserCreatedSerializer):
    class Meta:
        model = Transport
        fields = BaseCompanyUserCreatedSerializer.Meta.fields + [
            "name",
            "date",
            "vehicle_number",
            "type",
            "deliveries",
            "shipper",
        ]
        read_only_fields = BaseCompanyUserCreatedSerializer.Meta.read_only_fields
        extra_kwargs = {**BaseCompanyUserCreatedSerializer.Meta.extra_kwargs}
