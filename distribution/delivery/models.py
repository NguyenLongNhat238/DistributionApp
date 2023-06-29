from django.db import models
from constant.choice import TRANSPORT
from core_app.models import CompanyModelBase, Status
from user.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Delivery(CompanyModelBase):
    delivery_status = models.ForeignKey(
        Status,
        verbose_name=_("Delivery status"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="delivery_status_related",
        related_query_name="delivery_status",
    )
    shipper = models.ForeignKey(
        User,
        verbose_name=_("Shipper"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="delivery_shipper_related",
    )
    order = models.ForeignKey(
        "transaction.Order",
        verbose_name=_("Order"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="delivery_order_related",
    )
    delivery_date = models.DateTimeField(_("Delivery date"), null=True, blank=True)

    def __str__(self) -> str:
        if self.code:
            return f"{self.code}"
        if self.status:
            return self.status
        return super().__str__()

    class Meta:
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"


class DeliveryStatus(models.Model):
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        null=True,
        related_name="delivery_status_status_related",
        related_query_name="delivery_status_status",
    )
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.SET_NULL,
        null=True,
        related_name="delivery_status_delivery_related",
    )
    note = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self) -> str:
        if self.status and self.delivery:
            return f"{self.status}-{self.delivery}"
        return super().__str__()

    class Meta:
        verbose_name = "DeliveryStatus"
        verbose_name_plural = "DeliveryStatuses"


class Transport(CompanyModelBase):
    name = models.CharField(max_length=50)
    date = models.DateTimeField(null=True, blank=True)
    vehicle_number = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=TRANSPORT, default="CAR")

    deliveries = models.ManyToManyField(Delivery, blank=True)
    shipper = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="transport_shipper_related",
    )

    def __str__(self) -> str:
        if self.code:
            return f"{self.code}"
        if self.name:
            return self.name
        return super().__str__()
