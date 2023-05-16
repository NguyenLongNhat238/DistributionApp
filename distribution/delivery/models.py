from django.db import models
from constant.choice import TRANSPORT
from core_app.models import CompanyModelBase
from user.models import User
from datetime import datetime
# Create your models here.


class Status(CompanyModelBase):
    # TABLE_DELIVERY = "DELIVERY"
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    # entity = models.CharField()

    def __str__(self) -> str:
        if self.name:
            return self.name
        if self.code:
            return self.code

        return super().__str__()


class Delivery(CompanyModelBase):
    STATUS_DONE = 'Done'
    STATUS_WAITING = 'Waiting'
    STATUS_SHIPPING = 'Shipping'
    DELIVERY_STATUS = {
        (STATUS_DONE, 'Done'),
        (STATUS_WAITING, 'Shipping'),
        (STATUS_SHIPPING, 'Waiting')
    }
    delivery_status = models.CharField(
        max_length=50, choices=DELIVERY_STATUS, default=STATUS_WAITING)
    shipper = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='delivery_shipper_related')
    order = models.ForeignKey(
        "transaction.Order", on_delete=models.SET_NULL, null=True, related_name='delivery_order_related')
    delivery_date = models.DateTimeField(null=True, blank=True)

    def set_done(self):
        self.delivery_status = self.STATUS_DONE
        self.save()

    def set_shipping(self):
        self.delivery_status = self.STATUS_SHIPPING
        self.save()

    def set_waiting(self):
        self.delivery_status = self.STATUS_WAITING
        self.save()

    def __str__(self) -> str:
        if self.code:
            return f'{self.code}-{self.status}'
        if self.status:
            return self.status
        return super().__str__()


class DeliveryStatus(models.Model):
    status = models.ForeignKey(
        Status, on_delete=models.SET_NULL, null=True, related_name='delivery_status_status_related')
    delivery = models.ForeignKey(
        Delivery, on_delete=models.SET_NULL, null=True, related_name='delivery_status_delivery_related')
    note = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        if self.status and self.delivery:
            return f'{self.status}-{self.delivery}'
        return super().__str__()


class Transport(CompanyModelBase):
    name = models.CharField(max_length=50)
    date = models.DateTimeField(null=True, blank=True)
    vehicle_number = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=TRANSPORT, default="CAR")

    deliveries = models.ManyToManyField(Delivery, blank=True)
    shipper = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='transport_shipper_related')

    def __str__(self) -> str:
        if self.code:
            return f'{self.code}'
        if self.name:
            return self.name
        return super().__str__()
