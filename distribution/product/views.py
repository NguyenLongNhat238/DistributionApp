from django.shortcuts import render
from rest_framework import status, viewsets, permissions, generics
from rest_framework.response import Response

from core_app.permissions import BaseCompanyPermission
from core_app.views import BaseModelViewSet, ActionImportExcelViewSet
from .serializers import CategorySerializer, InventorySerializer, ProductDetailSerializer, ProductImportExcelSerializer, ProductSerializer, CategoryBaseSerializer
from .models import Category, Product, Inventory
# Create your views here.


class CategoryViewSet(BaseModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list']:
            return CategoryBaseSerializer
        return CategorySerializer


class ProductViewSet(BaseModelViewSet, ActionImportExcelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    import_serializer_class = ProductImportExcelSerializer
    add_exclude_fields = ("unit", "picture", "supplier")
    add_validate_fields = ("unit_name_char",
                           "unit_symbol_char", "supplier_name")
    model = Product
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return ProductDetailSerializer
        return ProductSerializer


class InventoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    # pagination_class = ListPaginator
    permission_classes = [permissions.IsAuthenticated]


class ListCurrenciesViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        pass
