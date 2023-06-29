from django.db import models
from core_app.models import CompanyModelBase, Status
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _

# Create your models here.


class OrderPayment(CompanyModelBase):
    payment_status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orderpayment_status_related",
        related_query_name="orderpayment_status",
    )
    order = models.ForeignKey(
        "transaction.Order",
        on_delete=models.SET_NULL,
        null=True,
        related_name="orderpayment_order_related",
        related_query_name="orderpayment_order",
    )
    payment_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    # Tiền khách trả
    paid_amount = MoneyField(
        _("Paid amount"),
        max_digits=14,
        decimal_places=3,
        default=0,
        default_currency="VND",
        help_text=_("This is paid amount of the order."),
    )
    # Tiền thừa
    # This is excess amount of the order after payment.
    excess_amount = MoneyField(
        _("Excess amount"),
        max_digits=14,
        decimal_places=3,
        default=0,
        default_currency="VND",
        null=True,
        blank=True,
        help_text=_("This is excess amount of the order after payment."),
    )
    # Tiền còn lại
    # This is remaining amount of the order after payment.
    remaining_amount = MoneyField(
        _("Remaining amount"),
        max_digits=14,
        decimal_places=3,
        default=0,
        default_currency="VND",
        null=True,
        blank=True,
        help_text=_("This is remaining amount of the order after payment."),
    )

    def __str__(self) -> str:
        if self.code:
            return f"{self.code}"
        if self.status:
            return self.status
        return super().__str__()

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"


class PurchasePayment(CompanyModelBase):
    payment_status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchasepayment_status_related",
        related_query_name="purchasepayment_status",
    )
    purchase = models.ForeignKey(
        "transaction.Purchase",
        on_delete=models.SET_NULL,
        null=True,
        related_name="purchasepayment_purchase_related",
        related_query_name="purchasepayment_purchase",
    )
    payment_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    # Tiền trả nhà cung cấp
    # This is paid amount of the purchase.
    paid_amount = MoneyField(
        _("Paid amount"),
        max_digits=14,
        decimal_places=3,
        default=0,
        default_currency="VND",
        help_text=_("This is paid amount of the purchase."),
    )
    # Tiền thừa sau khi trả
    # This is excess amount of the purchase after payment.
    excess_amount = MoneyField(
        _("Excess amount"),
        max_digits=14,
        decimal_places=3,
        default=0,
        default_currency="VND",
        null=True,
        blank=True,
        help_text=_("This is excess amount of the purchase after payment."),
    )
    # Tiền còn lại sau khi trả
    # This is remaining amount of the purchase after payment.
    remaining_amount = MoneyField(
        _("Remaining amount"),
        max_digits=14,
        decimal_places=3,
        default=0,
        default_currency="VND",
        null=True,
        blank=True,
        help_text=_("This is remaining amount of the purchase after payment."),
    )

    def __str__(self) -> str:
        if self.code:
            return f"{self.code}"
        if self.status:
            return self.status
        return super().__str__()

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
