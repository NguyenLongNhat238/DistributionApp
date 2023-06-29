from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.db import models
from core_app.models import CompanyModelBase, ModelBase
from information_management.models import Supplier
from user.models import User
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Category(CompanyModelBase):
    name = models.CharField(_("Name"), max_length=25)
    description = models.TextField(
        _("Description"), max_length=200, null=True, blank=True
    )

    def __str__(self) -> str:
        if self.code:
            return self.code
        if self.name:
            return self.name
        return super().__str__()

    class Meta:
        constraints = CompanyModelBase.Meta.constraints + [
            models.UniqueConstraint(
                fields=["name", "company"], name="unique_cate_name_company"
            ),
        ]

        verbose_name = "Category"
        verbose_name_plural = "Categories"


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class MeasurementUnit(CompanyModelBase):
    name = models.CharField(_("Name"), max_length=50, unique=True)
    symbol = models.CharField(
        _("Symbol"), max_length=10, unique=True, null=True, blank=True
    )

    class Meta:
        constraints = CompanyModelBase.Meta.constraints + [
            models.UniqueConstraint(
                fields=["name", "company"], name="unique_unit_name_company"
            ),
            models.UniqueConstraint(
                fields=["symbol", "company"], name="unique_unit_symbol_company"
            ),
        ]


class Product(CompanyModelBase):
    name = models.CharField(_("Name"), max_length=250)
    short_name = models.CharField(_("Short name"), max_length=25, null=True, blank=True)
    picture = models.ImageField(null=True, upload_to="products/%Y/%m", blank=True)
    brand = models.CharField(max_length=50, null=True, blank=True)
    specification = models.TextField(
        null=True,
        blank=True,
        help_text=_(
            "Enter detailed product information, including: size, weight, material, color, "
            "resolution, processing speed, storage capacity, operating system, ports and other features (if any)."
        ),
    )

    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    # unit product: túi, lít, kg, gói, hạt, chai
    unit = models.ForeignKey(
        MeasurementUnit, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Related to PURCHASE MODEL
    purchase_price = MoneyField(
        max_digits=14,
        decimal_places=3,
        default=0,
        default_currency="VND",
        help_text=_("This is the price of the imported product."),
        null=True,
        blank=True,
    )
    purchase_price_vat = MoneyField(
        max_digits=14,
        decimal_places=3,
        default=0,
        default_currency="VND",
        help_text=_("This is the price vat of the imported product."),
        null=True,
        blank=True,
    )

    price_novat_box = MoneyField(
        max_digits=14,
        decimal_places=3,
        default=0,
        default_currency="VND",
        null=True,
        blank=True,
        help_text=_("This is the price excluding VAT of the product sold in the box."),
    )
    price_novat_pcs = MoneyField(
        max_digits=14,
        decimal_places=3,
        default=0,
        default_currency="VND",
        null=True,
        blank=True,
        help_text=_("This is the price excluding VAT of the product sold by quantity."),
    )

    sold_price_vat_box = MoneyField(
        max_digits=14,
        decimal_places=3,
        default=0,
        default_currency="VND",
        null=True,
        blank=True,
        help_text=_("This is the price VAT of the product sold in the box."),
    )
    sold_price_vat_pcs = MoneyField(
        max_digits=14,
        decimal_places=3,
        default=0,
        default_currency="VND",
        null=True,
        blank=True,
        help_text=_("This is the price VAT of the product sold by quantity."),
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products_supplier_related",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_category_related",
    )

    def __str__(self) -> str:
        if self.code:
            return self.code
        if self.name:
            return self.name
        return super().__str__()

    def create_inventory(self):
        # You now have both access to self.id and self.name
        if self.id:
            inventory, _ = Inventory.objects.get_or_create(product_id=self.id)
            try:
                inventory.save()
            except BaseException as e:
                print(f"can't not save. Message: {str(e)}")
            print(f"created {inventory}")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_inventory()
        return True


class Inventory(CompanyModelBase):
    date = models.DateTimeField(null=True, blank=True)
    input_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    output_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    real_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    qty_box = models.IntegerField(null=True, blank=True)
    qty_bag = models.IntegerField(null=True, blank=True)
    real_qty_box = models.IntegerField(null=True, blank=True)
    real_qty_bag = models.IntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        null=True,
        related_name="inventory_product_related",
    )

    def __str__(self) -> str:
        if self.code:
            return self.code
        if self.product:
            return self.product
        return super().__str__()

    class Meta:
        verbose_name = "Inventories"
        verbose_name_plural = "Inventories"


class Warehouse(CompanyModelBase):
    purchase = models.ForeignKey(
        "transaction.Purchase",
        on_delete=models.CASCADE,
        null=True,
        related_name="warehouse_purchase_related",
    )
    date = models.DateTimeField(null=True, blank=True)
    inv_code = models.CharField(max_length=25)
    sap_code = models.CharField(max_length=25)
    truck_number = models.CharField(max_length=50)
    driver_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        if self.code:
            return self.code
        if self.truck_number:
            return self.truck_number
        return super().__str__()
