from django.apps import apps
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .get_username import get_request


class ActiveObjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="Active")


class StatusBase(models.Model):
    STATUS_ACTIVE = "Active"
    STATUS_INACTIVE = "Inactive"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_INACTIVE, "Inactive"),
    ]
    code = models.CharField(_("Code"), max_length=50, null=True, blank=True)
    status = models.CharField(
        _("Status"),
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )  # editable=False)

    slug = models.SlugField(
        _("Slug"),
        max_length=250,
        unique=True,
        default=uuid.uuid4,
        blank=True,
        editable=False,
    )

    objects = models.Manager()
    active_objects = ActiveObjectManager()

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
        settings.AUTH_USER_MODEL,
        db_constraint=False,
        on_delete=models.DO_NOTHING,
        verbose_name=("Created By"),
        related_name="%(app_label)s_%(class)s_created_by_related",
        related_query_name="%(app_label)s_%(class)s_created_by",
        blank=True,
        null=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True,
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_constraint=False,
        on_delete=models.DO_NOTHING,
        verbose_name=("Updated By"),
        related_name="%(app_label)s_%(class)s_updated_by_related",
        related_query_name="%(app_label)s_%(class)s_updated_by",
        blank=True,
        null=True,
        editable=False,
    )

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
                if class_name == "Company":
                    Company = apps.get_model("information_management", "Company")
                    count = Company.objects.last().id + 1
                elif class_name == "Customer":
                    Customer = apps.get_model("information_management", "Customer")
                    count = Customer.objects.last().id + 1
                elif class_name == "Employee":
                    Employee = apps.get_model("information_management", "Employee")
                    count = Employee.objects.last().id + 1
                elif class_name == "Supplier":
                    Supplier = apps.get_model("information_management", "Supplier")
                    count = Supplier.objects.last().id + 1

                # Delivery app
                elif class_name == "Delivery":
                    Delivery = apps.get_model("delivery", "Delivery")
                    count = Delivery.objects.last().id + 1
                elif class_name == "Status":
                    Status = apps.get_model("delivery", "Status")
                    count = Status.objects.last().id + 1
                elif class_name == "Transport":
                    Transport = apps.get_model("delivery", "Transport")
                    count = Transport.objects.last().id + 1

                # Product App
                elif class_name == "Product":
                    Product = apps.get_model("product", "Product")
                    count = Product.objects.last().id + 1
                elif class_name == "Category":
                    Category = apps.get_model("product", "Category")
                    count = Category.objects.last().id + 1
                elif class_name == "Inventory":
                    Inventory = apps.get_model("product", "Inventory")
                    count = Inventory.objects.last().id + 1
                elif class_name == "Warehouse":
                    Warehouse = apps.get_model("product", "Warehouse")
                    count = Warehouse.objects.last().id + 1
                elif class_name == "MeasurementUnit":
                    MeasurementUnit = apps.get_model("product", "MeasurementUnit")
                    count = MeasurementUnit.objects.last().id + 1

                # Transaction app
                elif class_name == "Order":
                    Order = apps.get_model("transaction", "Order")
                    count = Order.objects.last().id + 1
                elif class_name == "Purchase":
                    Purchase = apps.get_model("transaction", "Purchase")
                    count = Purchase.objects.last().id + 1
                elif class_name == "ExportedFile":
                    ExportedFile = apps.get_model("core_app", "ExportedFile")
                    count = ExportedFile.objects.last().id + 1
                else:
                    count = 0

            except:
                count = 1
            count_string = str(count).zfill(6)
            self.code = f"{class_name[0]}{count_string}"
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class CompanyManager(models.Manager):
    def get_queryset(self):
        request = get_request()
        if request:
            print("access")
            user = request.user
            if user.company:
                return super().get_queryset().filter(company=user.company)
            return super().get_queryset().filter(company=user.company_manager_related)
        return super().get_queryset()


class CompanyModelBase(ModelBase):
    company = models.ForeignKey(
        "information_management.Company",
        verbose_name=_("Company"),
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name="%(app_label)s_%(class)s_company_related",
        related_query_name="%(app_label)s_%(class)s_company",
        blank=True,
        null=True,
    )
    objects = models.Manager()
    company_objects = CompanyManager()

    def save(self, *args, **kwargs):
        request = get_request()
        try:
            if request:
                if not self.company:
                    if request.user.company:
                        self.company = request.user.company
                    elif request.user.company_manager_related:
                        self.company = request.user.company_manager_related
                    else:
                        Company = apps.get_model("information_management", "Company")
                        company = Company.objects.filter(manager=request.user).first()
                        self.company = company
        except:
            print("Can't not save company user")
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["code", "company"], name="unique_code_company_%(class)s"
            ),
        ]


def company_upload_to(instance, filename):
    request = get_request()
    company_id = None
    if request:
        if request.user:
            if request.user.company:
                company_id = request.user.company.id
            elif request.user.company_manager_related:
                company = request.user.company_manager_related
                company_id = company.id
    today = timezone.now().date()
    return f"exports/company_{company_id}/{today}/{filename}"


class ExportedFile(CompanyModelBase):
    file = models.FileField(_("File"), upload_to=company_upload_to)
    name_file = models.CharField(_("Name file"), max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        try:
            return self.file.name
        except:
            return super().__str__()


def get_related_model_choices():
    all_models = apps.get_models()
    related_model_choices = [
        (model.__name__.upper(), model.__name__)
        for model in all_models
        if model._meta.app_config.name
        in [
            "delivery",
            "product",
            "information_management",
            "payment",
            "transaction",
        ]
    ]
    return related_model_choices


class Status(CreationModificationDateBase):
    RELATED_MODEL_CHOICES = (
        # Delivery app
        ("Delivery", "Delivery"),
        ("DeliveryStatus", "DeliveryStatus"),
        ("Transport", "Transport"),
        # Information management app
        ("Company", "Company"),
        ("Supplier", "Supplier"),
        ("Employee", "Employee"),
        ("Customer", "Customer"),
        # Product app
        ("Category", "Category"),
        ("MeasurementUnit", "MeasurementUnit"),
        ("Product", "Product"),
        ("Inventory", "Inventory"),
        ("Warehouse", "Warehouse"),
        # Transaction app
        ("Order", "Order"),
        ("OrderDetail", "OrderDetail"),
        ("Purchase", "Purchase"),
        ("PurchaseDetail", "PurchaseDetail"),
        # Payment app
        ("OrderPayment", "OrderPayment"),
        ("PurchasePayment", "PurchasePayment"),
    )

    related_model = models.CharField(
        _("Related model"), max_length=100, choices=RELATED_MODEL_CHOICES
    )
    name = models.CharField(_("Status name"), max_length=50)
    description = models.TextField(_("Description"), null=True, blank=True)

    company = models.ForeignKey(
        "information_management.Company",
        verbose_name=_("Company"),
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name="company_status_related",
        related_query_name="company_status",
        blank=True,
        null=True,
    )

    objects = models.Manager()
    company_objects = CompanyManager()

    def save(self, *args, **kwargs):
        request = get_request()
        try:
            if request:
                if not self.company:
                    Company = apps.get_model("information_management", "Company")
                    company = Company.objects.filter(manager=request.user).first()
                    self.company = company
        except:
            print("Can't not save company user")
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class CompanyHistoryManager(models.Manager):
    def get_queryset(self):
        request = get_request()
        if request:
            user = request.user
            if user.company:
                return super().get_queryset().filter(company_id=user.company.id)
            return (
                super()
                .get_queryset()
                .filter(company_id=user.company_manager_related.id)
            )
        return super().get_queryset()


class History(models.Model):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

    ACTION_CHOICES = (
        (CREATE, "Create"),
        (UPDATE, "Update"),
        (DELETE, "Delete"),
    )

    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    company_id = models.PositiveIntegerField(null=True, blank=True)
    data = models.JSONField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    company_objects = CompanyHistoryManager()

    def __str__(self):
        return f"{self.action} - {self.model_name} - {self.object_id}"

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "History"
        verbose_name_plural = "Histories"
