from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from core_app.models import ExportedFile

# Register your models here.


class BaseAdminSite(admin.ModelAdmin):
    list_display = ("code", "id")
    list_select_related = ("company",)


admin.site.register(ExportedFile)
