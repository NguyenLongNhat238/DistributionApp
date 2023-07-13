import json
from datetime import datetime


def add_single_table(model: object, data: list):
    for item in data:
        if item and item != "" and item != "*":
            record, created = model.all_objects.get_or_create(name=item)
            if created:
                record.save()


class RelatedMixin:
    @classmethod
    def load_related(cls, queryset):
        """
        This function allow dynamic addition of the related objects to
        the provided query.
        @parameter param1: queryset
        """
        if hasattr(cls, "select_related_fields"):
            if len(cls.select_related_fields) > 0:
                queryset = queryset.select_related(*cls.select_related_fields)
        if hasattr(cls, "prefetch_related_fields"):
            if len(cls.prefetch_related_fields) > 0:
                queryset = queryset.prefetch_related(*cls.prefetch_related_fields)
        if hasattr(cls, "sort_fields"):
            if len(cls.sort_fields) > 0:
                queryset = queryset.order_by(*cls.sort_fields)
        return queryset


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
