from django.shortcuts import render
from rest_framework import permissions, viewsets, generics
from rest_framework.response import Response
from .models import OrderPayment, PurchasePayment
from .serializers import OrderPaymentSerializer, OrderPaymentDetailSerialzier
from core_app.views import BaseModelViewSet

# Create your views here.


class OrderPaymentViewSet(BaseModelViewSet):
    queryset = OrderPayment.company_objects.all()
    serializer_class = OrderPaymentSerializer
    model = OrderPayment
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderPaymentDetailSerialzier
        return super().get_serializer_class()


class PurchasePaymentViewSet(BaseModelViewSet):
    queryset = PurchasePayment.company_objects.all()
    serializer_class = OrderPaymentSerializer
    model = PurchasePayment
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderPaymentDetailSerialzier
        return super().get_serializer_class()
