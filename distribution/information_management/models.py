from django.core.validators import RegexValidator
from django.db import models
from core_app.get_username import get_request
from core_app.models import ModelBase, CompanyModelBase
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.


class Company(ModelBase):
    name = models.CharField(_("Company name"), max_length=50)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("List users member"),
        blank=True,
        related_name="company_users_related",
    )
    detail = models.TextField(_("Detail"), null=True, blank=True)
    manager = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Manager"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="company_manager_related",
    )

    def __str__(self) -> str:
        if self.name:
            return self.name
        return super().__str__()

    def save(self, *args, **kwargs):
        request = get_request()
        try:
            if request:
                self.manager = request.user
        except:
            print("Can't not save company user")
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


class Supplier(CompanyModelBase):
    name = models.CharField(_("Supplier name"), max_length=100)
    address = models.TextField(_("Suplier address"), null=True, blank=True)
    tax_code = models.CharField(_("Tax code"), max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        if self.code:
            return self.code
        if self.name:
            return self.name
        return super().__str__()

    class Meta:
        constraints = CompanyModelBase.Meta.constraints + [
            models.UniqueConstraint(
                fields=["name", "company"], name="unique_supplier_name_company"
            ),
        ]


class Employee(CompanyModelBase):
    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50, null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=50)
    address = models.TextField(_("Address"), null=True, blank=True)

    @property
    def full_name(self):
        "Returns the person's full name."
        if self.first_name:
            return "%s %s" % (self.last_name, self.first_name)

        return None

    def __str__(self) -> str:
        if self.code:
            return self.code
        if self.first_name:
            return self.first_name
        return super().__str__()


class Customer(CompanyModelBase):
    first_name = models.CharField(_("First name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("Last name"), max_length=75, null=True, blank=True)
    shop_name = models.CharField(_("Shop name"), max_length=100, null=True, blank=True)
    house_number = models.CharField(
        _("House number"), max_length=25, null=True, blank=True
    )
    # location
    city = models.CharField(
        _("City"), max_length=100, null=True, blank=True
    )  # thành phố
    district = models.CharField(
        _("District"), max_length=100, null=True, blank=True
    )  # quận/ huyện
    ward = models.CharField(
        _("Ward"), max_length=100, null=True, blank=True
    )  # phường/ xã
    # Ghi chú thêm: ví dụ đường quốc lộ 56, tổ dân cư, hẻm nhà, số nhà
    street = models.CharField(_("Street"), max_length=200, null=True, blank=True)
    full_address = models.TextField(_("Full address"), null=True, blank=True)

    # Validators should be a list
    phone_number = models.CharField(
        _("Phone number"), max_length=50, blank=True, null=True
    )
    notes = models.TextField(_("Notes"), null=True, blank=True)
    channel = models.ForeignKey(
        "Channel",
        verbose_name=_("Channel"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    @property
    def full_name(self):
        "Returns the person's full name."
        if self.first_name:
            return "%s %s" % (self.last_name, self.first_name)
        # elif self.username:
        #     return self.username
        if self.shop_name:
            return self.shop_name
        return None

    def __str__(self) -> str:
        if self.code:
            return self.code
        if self.first_name:
            return self.first_name
        return super().__str__()


class Channel(CompanyModelBase):
    name = models.CharField(_("Channel name"), max_length=100)
    description = models.TextField(_("Description"), null=True, blank=True)

    def __str__(self) -> str:
        if self.code:
            return self.code
        if self.name:
            return self.name
        return super().__str__()

    class Meta:
        constraints = CompanyModelBase.Meta.constraints + [
            models.UniqueConstraint(
                fields=["name", "company"], name="unique_channel_name_company"
            ),
        ]
