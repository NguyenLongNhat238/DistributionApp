from rest_framework import serializers
from django.db.models import Avg
from core_app.serializers import BaseModelUserCreatedSerializer, CompanyModelBaseSerializer
from information_management.models import Company, Supplier
from information_management.serializers import SupplierBaseSerializer
from .models import MeasurementUnit, Product, Inventory, Warehouse, Category


class CategoryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "code", "name"]


class CategorySerializer(CompanyModelBaseSerializer, BaseModelUserCreatedSerializer):
    class Meta:
        model = Category
        fields = CompanyModelBaseSerializer.Meta.fields + BaseModelUserCreatedSerializer.Meta.fields + \
            ["name", "description"]

        read_only_fields = BaseModelUserCreatedSerializer.Meta.read_only_fields + \
            CompanyModelBaseSerializer.Meta.read_only_fields
        extra_kwargs = {**CompanyModelBaseSerializer.Meta.extra_kwargs,
                        **BaseModelUserCreatedSerializer.Meta.extra_kwargs}


class ProductSerializer(CompanyModelBaseSerializer, BaseModelUserCreatedSerializer):
    class Meta:
        model = Product
        fields = CompanyModelBaseSerializer.Meta.fields + BaseModelUserCreatedSerializer.Meta.fields + \
            ["name", "short_name", "unit", "supplier", "category",
             "picture", "brand", "specification",
             "weight", "height", "length", "width",
             "purchase_price", "purchase_price_vat", "price_novat_box", "price_novat_pcs", "sold_price_vat_box", "sold_price_vat_pcs"]

        read_only_fields = BaseModelUserCreatedSerializer.Meta.read_only_fields + \
            CompanyModelBaseSerializer.Meta.read_only_fields
        extra_kwargs = {**CompanyModelBaseSerializer.Meta.extra_kwargs,
                        **BaseModelUserCreatedSerializer.Meta.extra_kwargs}


class ProductImportExcelSerializer(ProductSerializer):
    supplier_name = serializers.CharField(max_length=50, required=True)
    unit_name_char = serializers.CharField(
        max_length=50, required=False, allow_null=True)
    unit_symbol_char = serializers.CharField(
        max_length=50, required=False, allow_null=True)

    def validate_supplier_name(self, value):

        if value:
            supplier, _ = Supplier.objects.get_or_create(name=value)
            self.supplier = supplier.id

        return supplier.id

    def create(self, validated_data):
        unit_name = validated_data.pop('unit_name_char', None)
        unit_symbol_char = validated_data.pop('unit_symbol_char', None)
        supplier_name = validated_data.pop('supplier_name', None)
        unit = None
        if unit_name:
            unit = MeasurementUnit.objects.filter(
                name=unit_name)
            if unit:
                self.unit = unit
            else:
                unit = MeasurementUnit.objects.create(
                    name=unit_name, symbol=unit_symbol_char)
                unit.save()
                self.unit = unit
        product = Product.objects.create(
            **validated_data, unit=unit, supplier_id=supplier_name)
        return product

    class Meta:
        model = ProductSerializer.Meta.model
        fields = ProductSerializer.Meta.fields + \
            ['supplier_name', 'unit_name_char',
                'unit_symbol_char']


class ProductDetailSerializer(ProductSerializer):
    supplier = SupplierBaseSerializer(read_only=True)
    category = CategoryBaseSerializer(read_only=True)
    # purchase_price_format = serializers.SerializerMethodField()
    # sold_price_retail_format = serializers.SerializerMethodField()

    # def get_sold_price_retail_format(self, obj):
    #     return obj.sold_price_retail.__str__()

    # def get_purchase_price_format(self, obj):
    #     return obj.purchase_price.__str__()

    class Meta:
        model = ProductSerializer.Meta.model
        fields = ProductSerializer.Meta.fields + \
            ["purchase_price_currency", "purchase_price_vat_currency", "price_novat_box_currency",
                "price_novat_pcs_currency", "sold_price_vat_box_currency", "sold_price_vat_pcs_currency"]
        read_only = True


class InventorySerializer(CompanyModelBaseSerializer, BaseModelUserCreatedSerializer):
    class Meta:
        model = Inventory
        fields = CompanyModelBaseSerializer.Meta.fields + \
            BaseModelUserCreatedSerializer.Meta.fields + \
            ["date", "input_quantity", "output_quantity", "real_quantity", "qty_box", "qty_bag",
                "real_qty_box", "real_qty_bag", "note", "product"]

        read_only_fields = BaseModelUserCreatedSerializer.Meta.read_only_fields + \
            CompanyModelBaseSerializer.Meta.read_only_fields
        extra_kwargs = {**CompanyModelBaseSerializer.Meta.extra_kwargs,
                        **BaseModelUserCreatedSerializer.Meta.extra_kwargs}
