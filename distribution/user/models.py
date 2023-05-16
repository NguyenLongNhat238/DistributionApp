from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Q
from django.core.validators import RegexValidator
import jwt
from PIL import Image


class User(AbstractUser):
    NONE = "None"

    # Sex
    SEX_MALE = "Male"
    SEX_FEMALE = "Female"
    SEX = (
        (SEX_MALE, 'Male'),
        (SEX_FEMALE, 'Female'),
        (NONE, 'None')
    )

    # Role
    ROLE_SYSTEM_ADDMIN = "System admin"
    ROLE_SHIPPER = "Shipper"
    ROLE = (
        (NONE, 'None'),
        (ROLE_SYSTEM_ADDMIN, 'System admin'),
        (ROLE_SHIPPER, 'Shipper'),)

    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(_('email address'), max_length=50, unique=True)
    phone_regex = RegexValidator(
        regex=r'^(0|84)(2(0[3-9]|1[0-6|8|9]|2[0-2|5-9]|3[2-9]|4[0-9]|5[1|2|4-9]|6[0-3|9]|7[0-7]|8[0-9]|9[0-4|6|7|9])|3[2-9]|5[5|6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])([0-9]{7})$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(_('phone number'), validators=[
                             phone_regex], max_length=17, unique=True)  # validators should be a list

    auth_google = models.BooleanField(default=False)
    auth_facebook = models.BooleanField(default=False)

    birthday = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=6, choices=SEX, default=NONE)
    # role user for dev
    role = models.CharField(max_length=12, choices=ROLE, default=NONE)
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m', blank=True)
    identity_card = models.CharField(max_length=25, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)  # thành phố
    district = models.CharField(
        max_length=100, null=True, blank=True)  # quận/ huyện
    ward = models.CharField(max_length=100, null=True,
                            blank=True)  # phường/ xã
    # Ghi chú thêm: ví dụ đường quốc lộ 56, tổ dân cư, hẻm nhà, số nhà
    street = models.CharField(max_length=200, null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'username']

    def __str__(self):
        return self.phone

    def set_system_admin(self):
        self.role = self.ROLE_SYSTEM_ADDMIN
        self.save()

    def set_role_shipper(self):
        self.role = self.ROLE_SHIPPER
        self.save()

    def set_role_none(self):
        self.role = self.NONE
        self.save()

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
        if self.first_name:
            return '%s %s' % (self.last_name, self.first_name)
        # elif self.username:
        #     return self.username
        if self.email:
            return self.email.split("@")[0]
        return self.phone

    @property
    def access_token(self):
        '''
            access token for user login
        '''
        token = jwt.encode({'id': self.id, 'type': 'access_token', 'username': self.username, 'email': self.email,
                           'exp': datetime.utcnow() + timedelta(days=1)}, settings.SECRET_KEY, algorithm='HS256')
        return token

    @property
    def refresh_token(self):
        '''
            refresh token for user login
        '''
        token = jwt.encode({'id': self.id, 'type': 'refresh_token', 'username': self.username, 'email': self.email,
                           'exp': datetime.utcnow() + timedelta(days=27)}, settings.SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def activate_token(username, email, random_code):
        '''
            activate token for activating account
        '''
        token = jwt.encode({'type': 'activate_token', 'username': username, 'email': email, 'random_code': random_code,
                           'exp': datetime.utcnow() + timedelta(minutes=5)}, settings.SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def reset_password_token(user):
        '''
            reset_password_token for reset password when user forgot password
        '''
        token = jwt.encode({'id': user.id, 'type': 'reset_password_token', 'username': user.username, 'email': user.email,
                           'exp': datetime.utcnow() + timedelta(minutes=45)}, settings.SECRET_KEY, algorithm='HS256')
        return token
