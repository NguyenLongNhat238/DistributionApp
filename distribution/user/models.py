from collections.abc import Iterable
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import RegexValidator
import jwt
from information_management.models import Company


class User(AbstractUser):
    NONE = "None"

    # Sex
    SEX_MALE = "Male"
    SEX_FEMALE = "Female"
    SEX = ((SEX_MALE, "Male"), (SEX_FEMALE, "Female"), (NONE, "None"))

    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(_("email address"), max_length=50, unique=True)
    phone_regex = RegexValidator(
        regex=r"^(0|84)(2(0[3-9]|1[0-6|8|9]|2[0-2|5-9]|3[2-9]|4[0-9]|5[1|2|4-9]|6[0-3|9]|7[0-7]|8[0-9]|9[0-4|6|7|9])|3[2-9]|5[5|6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])([0-9]{7})$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone = models.CharField(
        _("phone number"), validators=[phone_regex], max_length=17, unique=True
    )  # validators should be a list

    auth_google = models.BooleanField(default=False)
    auth_facebook = models.BooleanField(default=False)

    birthday = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=6, choices=SEX, default=NONE)

    role = models.ForeignKey(
        "system_admin.UserRole",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_role_related",
        related_query_name="user_role",
    )
    avatar = models.ImageField(null=True, upload_to="users/%Y/%m", blank=True)
    identity_card = models.CharField(max_length=25, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=False)

    company = models.ForeignKey(
        "information_management.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_company_related",
        related_query_name="user_company",
        verbose_name=_("Company"),
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email", "username"]

    def __str__(self):
        return self.phone

    def is_system_admin(self) -> bool:
        return self.role.is_system_admin()

    def is_system_employee(self) -> bool:
        return self.role.is_system_employee()

    def is_shipper(self) -> bool:
        return self.role.is_shipper()

    def is_company_manager(self):
        if Company.objects.filter(manager=self).exists():
            return True
        return None

    @property
    def role_name(self):
        if self.role:
            return self.role.name
        return None

    @property
    def role_code(self):
        if self.role:
            return self.role.code
        return None

    def has_permissions(self, permission):
        """
        Check if user has permissions
        """
        if self.role:
            return self.role.has_permissions(permission)
        return False

    def has_user_management_permission(self):
        return self.role.has_user_management_permission()

    def set_sex_male(self):
        self.sex = self.SEX_MALE
        self.save()

    def set_sex_female(self):
        self.sex = self.SEX_FEMALE
        self.save()

    def set_sex_none(self):
        self.sex = self.NONE
        self.save()

    @property
    def full_name(self):
        "Returns the person's full name."
        if self.first_name and self.last_name:
            return "%s %s" % (self.last_name, self.first_name)
        if self.username:
            return self.username
        if self.email:
            return self.email.split("@")[0]
        return self.phone

    @property
    def access_token(self):
        """
        access token for user login
        """
        token = jwt.encode(
            {
                "id": self.id,
                "type": "access_token",
                "username": self.username,
                "email": self.email,
                "exp": timezone.now() + timedelta(days=1),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return token

    @property
    def refresh_token(self):
        """
        refresh token for user login
        """
        token = jwt.encode(
            {
                "id": self.id,
                "type": "refresh_token",
                "username": self.username,
                "email": self.email,
                "exp": timezone.now() + timedelta(days=27),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return token

    @staticmethod
    def activate_token(username, email, random_code):
        """
        activate token for activating account
        """
        token = jwt.encode(
            {
                "type": "activate_token",
                "username": username,
                "email": email,
                "random_code": random_code,
                "exp": timezone.now() + timedelta(minutes=5),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return token

    @staticmethod
    def reset_password_token(user):
        """
        reset_password_token for reset password when user forgot password
        """
        token = jwt.encode(
            {
                "id": user.id,
                "type": "reset_password_token",
                "username": user.username,
                "email": user.email,
                "exp": timezone.now() + timedelta(minutes=45),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return token
