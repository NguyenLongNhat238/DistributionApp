from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from .models import User
from django.utils.html import mark_safe, format_html


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
        field_classes = {"email": forms.EmailField}

    # placeholders = ['example@email.com', 'Username', ]


@admin.register(User)
class UserDisplay(UserAdmin):
    def image_admin(self, obj):
        if obj:
            return mark_safe(
                '<img src="/media/{url}" width="240" />'.format(url=obj.avatar.name)
            )

    save_on_top = True

    fieldsets = (
        (None, {"fields": ("phone", "username", "password", "role", "company")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            ("Public information"),
            {
                "fields": (
                    "avatar",
                    "image_admin",
                    "birthday",
                    "sex",
                )
            },
        ),
        (
            ("Information address"),
            {"fields": ("identity_card", "address", "status")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "phone",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    readonly_fields = ["image_admin"]
    # form = CustomUserCreationForm
    add_form = CustomUserCreationForm

    list_display = (
        "id",
        "phone",
        "email",
        "username",
        "date_joined",
        "last_login",
        "auth_google",
        "status",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("email", "phone")
