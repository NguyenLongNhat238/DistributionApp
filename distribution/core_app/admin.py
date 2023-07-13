from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from information_management.models import Company

from core_app.models import ExportedFile, History

# Register your models here.


class BaseAdminSite(admin.ModelAdmin):
    list_display = ("code", "id")
    list_select_related = ("company",)


class HistoryAdminSite(admin.ModelAdmin):
    list_display = ("id", "action", "model_name", "object_id", "company_id", "user")
    readonly_fields = ("timestamp",)


admin.site.register(ExportedFile)
admin.site.register(History, HistoryAdminSite)
admin.site.site_header = "DISTRIBUTIONS"
admin.site.index_title = "Management Area"
admin.site.site_title = "Distributions"
admin.site.site_url = ""
