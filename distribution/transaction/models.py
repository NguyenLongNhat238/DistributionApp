from decimal import Decimal
from django.db import models
from core_app.models import ModelBase, CompanyModelBase
from information_management.models import Customer, Supplier, Employee
from product import models as pro_models
from djmoney.models.fields import MoneyField
# Create your models here.


class Order(CompanyModelBase):
    # status =
    est_delivery_date = models.DateTimeField(null=True, blank=True)
    order_date = models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, related_name='oders_customer_related')
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name='oders_employee_related')

    def __str__(self) -> str:
        if self.code:
            return self.code
        if self.customer:
            return self.customer
        return super().__str__()


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, related_name='order_detail_order_related')
    product = models.ForeignKey(
        pro_models.Product, on_delete=models.CASCADE, null=True, related_name='order_detail_product_related')
    quantity_box = models.FloatField(null=True, blank=True)
    quantity_promo_box = models.FloatField(null=True, blank=True)
    quantity_pcs = models.FloatField(null=True, blank=True)
    quantity_promo_pcs = models.FloatField(null=True, blank=True)

    total_quantity_pcs = models.FloatField(null=True, blank=True)
    total_quantity_promo_pcs = models.FloatField(null=True, blank=True)

    display_amount = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')

    discount = models.DecimalField(
        max_digits=3, decimal_places=3, default=Decimal(0), null=True, blank=True, validators=pro_models.PERCENTAGE_VALIDATOR)
    discount_novat_price = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')

    base_discount = models.DecimalField(
        max_digits=3, decimal_places=3, default=Decimal(0), null=True, blank=True, validators=pro_models.PERCENTAGE_VALIDATOR)
    base_discount_amount = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')

    discount_shop = models.DecimalField(
        max_digits=3, decimal_places=3, default=Decimal(0), null=True, blank=True, validators=pro_models.PERCENTAGE_VALIDATOR)
    discount_shop_amount = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')

    price_box = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')
    price_pcs = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')
    total_price = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')
    price_after_discount = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')

    def __str__(self) -> str:
        return super().__str__()

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class Purchase(CompanyModelBase):
    est_delivery_date = models.DateTimeField(null=True, blank=True)
    purchase_date = models.DateTimeField(null=True, blank=True)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True, related_name='purchases_customer_related')
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name='purchases_employee_related')

    def __str__(self) -> str:
        if self.code:
            return self.code
        return super().__str__()


class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE, null=True, related_name='purchase_detail_purchase_related')
    product = models.ForeignKey(
        pro_models.Product, on_delete=models.CASCADE, null=True, related_name='purchase_detail_product_related')
    quantity_box = models.FloatField(null=True, blank=True)
    quantity_promo_box = models.FloatField(null=True, blank=True)
    quantity_pcs = models.FloatField(null=True, blank=True)
    quantity_promo_pcs = models.FloatField(null=True, blank=True)

    total_quantity_pcs = models.FloatField(null=True, blank=True)
    total_quantity_promo_pcs = models.FloatField(null=True, blank=True)

    display_amount = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')

    discount = models.DecimalField(
        max_digits=3, decimal_places=2, default=Decimal(0), validators=pro_models.PERCENTAGE_VALIDATOR)
    discount_novat_price = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')

    base_discount = models.DecimalField(
        max_digits=3, decimal_places=2, default=Decimal(0), validators=pro_models.PERCENTAGE_VALIDATOR)
    base_discount_amount = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')

    discount_shop = models.DecimalField(
        max_digits=3, decimal_places=2, default=Decimal(0), validators=pro_models.PERCENTAGE_VALIDATOR)
    discount_shop_amount = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')

    price_box = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')
    price_pcs = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')
    total_price = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')
    price_after_discount = MoneyField(
        max_digits=14, decimal_places=3, null=True, blank=True, default_currency='VND')

    def __str__(self) -> str:
        return super().__str__()

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
