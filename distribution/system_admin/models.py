from django.db import models
from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from core_app.get_username import get_request
from core_app.models import CompanyManager

# Create your models here.


class UserRole(models.Model):
    NONE = "none"
    ROLE_SYSTEM_ADDMIN = "system_admin"
    ROLE_SYSTEM_EMPLOYEE = "system_employee"
    ROLE_SHIPPER = "shipper"

    ROLE = (
        (NONE, "None"),
        (ROLE_SYSTEM_ADDMIN, "System admin"),
        (ROLE_SYSTEM_EMPLOYEE, "System employee"),
        (ROLE_SHIPPER, "Shipper"),
    )
    name = models.CharField(_("Role name"), max_length=100)
    code = models.CharField(_("Role code"), choices=ROLE, max_length=100)
    permissions = models.ManyToManyField(
        "Permission", verbose_name=_("Permission"), blank=True
    )
    description = models.TextField(_("Description"), null=True, blank=True)

    company = models.ForeignKey(
        "information_management.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_role_company_related",
        related_query_name="user_role_company",
        verbose_name=_("Company"),
    )

    objects = models.Manager()
    company_objects = CompanyManager()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        request = get_request()
        if request:
            if not self.company:
                if request.user.company:
                    self.company = request.user.company
        return super().save(*args, **kwargs)

    @property
    def get_permissions_code(self):
        return self.permissions.all().values_list("code", flat=True)

    # this function is used to check if user has permission
    def has_permissions(self, permission_code):
        return permission_code in self.get_permissions_code

    # this function is used to check if user has user management permission
    def has_user_management_permission(self):
        return self.has_permissions("user_management")

    # this function is check if user is system admin
    def is_system_admin(self) -> bool:
        return self.code == self.ROLE_SYSTEM_ADDMIN

    # this function is check if user is system employee
    def is_system_employee(self) -> bool:
        return self.code == self.ROLE_SYSTEM_EMPLOYEE

    # this function is check if user is shipper
    def is_shipper(self) -> bool:
        return self.code == self.ROLE_SHIPPER

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "company"], name="unique_code_company_%(class)s"
            ),
        ]


class Permission(models.Model):
    ACTION = ["View", "Add", "Change", "Delete"]
    ORDER = {
        "key": "order",
        "name": "Order",
    }
    PRODUCT = {
        "key": "product",
        "name": "Product",
    }
    USER = {
        "key": "user",
        "name": "User",
    }
    PAYMENT = {
        "key": "payment",
        "name": "Payment",
    }
    DELIVERY = {
        "key": "delivery",
        "name": "Delivery",
    }
    INFORMATION_MANAGEMENT = {
        "key": "information_management",
        "name": "Information management",
    }
    TRANSACTION = {
        "key": "transaction",
        "name": "Transaction",
    }

    name = models.CharField(_("Permission name"), max_length=100, unique=True)
    code = models.CharField(_("Permission code"), max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


@receiver(post_migrate)
def create_default_permissions(sender, **kwargs):
    if sender.name == "system_admin":  # replace 'system_admin' with your app name
        Permission = apps.get_model(
            "system_admin", "Permission"
        )  # replace 'system_admin' with your app name
        if not Permission.objects.exists():
            # Create default permissions
            for item in Permission.ACTION:
                Permission.objects.create(
                    name=f"{item} {Permission.ORDER['name']}",
                    code=f"{item}_{Permission.ORDER['key']}",
                )
                Permission.objects.create(
                    name=f"{item} {Permission.PRODUCT['name']}",
                    code=f"{item}_{Permission.PRODUCT['key']}",
                )
                Permission.objects.create(
                    name=f"{item} {Permission.USER['name']}",
                    code=f"{item}_{Permission.USER['key']}",
                )
                Permission.objects.create(
                    name=f"{item} {Permission.PAYMENT['name']}",
                    code=f"{item}_{Permission.PAYMENT['key']}",
                )
                Permission.objects.create(
                    name=f"{item} {Permission.DELIVERY['name']}",
                    code=f"{item}_{Permission.DELIVERY['key']}",
                )
                Permission.objects.create(
                    name=f"{item} {Permission.INFORMATION_MANAGEMENT['name']}",
                    code=f"{item}_{Permission.INFORMATION_MANAGEMENT['key']}",
                )
                Permission.objects.create(
                    name=f"{item} {Permission.TRANSACTION['name']}",
                    code=f"{item}_{Permission.TRANSACTION['key']}",
                )
