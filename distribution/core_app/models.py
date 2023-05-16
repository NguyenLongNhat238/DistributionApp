from django.apps import apps
import uuid
from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import FieldError, ValidationError
from django.template.defaultfilters import slugify

# from simple_history.models import HistoricalRecords

from .get_username import get_request


class ActiveObjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='Active')


class StatusBase(models.Model):
    STATUS_ACTIVE = 'Active'
    STATUS_INACTIVE = 'Inactive'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
    ]
    code = models.CharField(_("Code"), unique=True,
                            max_length=50, null=True, blank=True)
    status = models.CharField(_('Status'), max_length=50,
                              choices=STATUS_CHOICES, default=STATUS_ACTIVE, )  # editable=False)

    slug = models.SlugField(_("Slug"), max_length=250,
                            unique=True, default=uuid.uuid4, blank=True, editable=False)

    active_objects = ActiveObjectManager()
    objects = models.Manager()

    class Meta:
        abstract = True

    def activate(self):
        self.record_status = self.STATUS_ACTIVE
        self.save()

    def deactivate(self):
        self.record_status = self.STATUS_INACTIVE
        self.save()


class CreationModificationDateBase(models.Model):
    """
    Abstract base class with a creation and modification date and time
    """

    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, db_constraint=False, on_delete=models.DO_NOTHING,
        verbose_name=("Created By"),
        related_name="%(app_label)s_%(class)s_created_by_related",
        related_query_name="%(app_label)s_%(class)s_created_by",
        blank=True, null=True, editable=False)

    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True,
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, db_constraint=False, on_delete=models.DO_NOTHING,
        verbose_name=("Updated By"),
        related_name="%(app_label)s_%(class)s_updated_by_related",
        related_query_name="%(app_label)s_%(class)s_updated_by",
        blank=True, null=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        request = get_request()
        if request:
            if not self.created_by:
                self.created_by = request.user
            self.updated_by = request.user
        return super().save(*args, **kwargs)


class ModelBase(CreationModificationDateBase, StatusBase):

    def save(self, *args, **kwargs):

        if self.code is None:
            class_name = self._meta.object_name
            try:
                # Information management app
                if class_name == 'Company':
                    Company = apps.get_model(
                        'information_management', 'Company')
                    count = Company.objects.last().id + 1
                elif class_name == 'Customer':
                    Customer = apps.get_model(
                        'information_management', 'Customer')
                    count = Customer.objects.last().id + 1
                elif class_name == 'Employee':
                    Employee = apps.get_model(
                        'information_management', 'Employee')
                    count = Employee.objects.last().id + 1
                elif class_name == 'Supplier':
                    Supplier = apps.get_model(
                        'information_management', 'Supplier')
                    count = Supplier.objects.last().id + 1

                # Delivery app
                elif class_name == 'Delivery':
                    Delivery = apps.get_model('delivery', 'Delivery')
                    count = Delivery.objects.last().id + 1
                elif class_name == 'Status':
                    Status = apps.get_model('delivery', 'Status')
                    count = Status.objects.last().id + 1
                elif class_name == 'Transport':
                    Transport = apps.get_model('delivery', 'Transport')
                    count = Transport.objects.last().id + 1

                # Product App
                elif class_name == 'Product':
                    Product = apps.get_model('product', 'Product')
                    count = Product.objects.last().id + 1
                elif class_name == 'Category':
                    Category = apps.get_model('product', 'Category')
                    count = Category.objects.last().id + 1
                elif class_name == 'Inventory':
                    Inventory = apps.get_model('product', 'Inventory')
                    count = Inventory.objects.last().id + 1
                elif class_name == 'Warehouse':
                    Warehouse = apps.get_model('product', 'Warehouse')
                    count = Warehouse.objects.last().id + 1
                elif class_name == 'MeasurementUnit':
                    MeasurementUnit = apps.get_model(
                        'product', 'MeasurementUnit')
                    count = MeasurementUnit.objects.last().id + 1

                # Transaction app
                elif class_name == 'Order':
                    Order = apps.get_model('transaction', 'Order')
                    count = Order.objects.last().id + 1
                elif class_name == 'Purchase':
                    Purchase = apps.get_model('transaction', 'Purchase')
                    count = Purchase.objects.last().id + 1

                else:
                    count = 0

            except:
                count = 1
            count_string = str(count).zfill(6)
            self.code = f'{class_name[0]}{count_string}'
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class CompanyManager(models.Manager):
    def get_queryset(self):
        request = get_request()
        user = request.user
        return super().get_queryset().filter(company=user.company_manager)


class CompanyModelBase(ModelBase):
    company = models.ForeignKey(
        "information_management.Company", on_delete=models.DO_NOTHING, db_constraint=False,
        related_name="%(app_label)s_%(class)s_company_related",
        related_query_name="%(app_label)s_%(class)s_company",
        blank=True, null=True)

    company_objects = CompanyManager()

    def save(self, *args, **kwargs):
        request = get_request()
        try:
            if request:
                if not self.company:
                    Company = apps.get_model(
                        'information_management', 'Company')
                    company = Company.objects.filter(
                        manager=request.user).first()
                    self.company = company
        except:
            print("Can't not save company user")
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
