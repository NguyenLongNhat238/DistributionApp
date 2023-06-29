from django.shortcuts import render
from rest_framework import permissions, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from core_app.views import BaseModelViewSet
from .models import Delivery, DeliveryStatus, Transport
from .serializers import (
    DeliverySerializer,
    DeliveryStatusParamSerializer,
    DeliveryStatusSerializer,
    TransportSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.


class DeliveryViewSet(BaseModelViewSet):
    queryset = Delivery.company_objects.all()
    serializer_class = DeliverySerializer
    model = Delivery
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return super().get_serializer_class()


class DeliveryStatusViewSet(
    viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    queryset = DeliveryStatus.objects.all()
    serializer_class = DeliveryStatusSerializer
    model = DeliveryStatus
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_queryset(self):
        query = DeliveryStatus.objects.all()
        params = self.request.query_params
        serializer = DeliveryStatusParamSerializer(data=params)
        serializer.is_valid(raise_exception=True)
        query = query.filter(delivery_id=serializer.validated_data["delivery_id"])
        return query

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="delievery_id",
                required=True,
                in_=openapi.IN_QUERY,
                description="delivery id to filter delivery status (required)",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TransportViewSet(BaseModelViewSet):
    queryset = Transport.company_objects.all()
    serializer_class = TransportSerializer
    model = Transport
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return super().get_serializer_class()
