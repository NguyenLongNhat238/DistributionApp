from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import History
from .get_username import get_request
from django.forms.models import model_to_dict

LIST_LABEL = [
    "information_management",
    "delivery",
    "notification",
    "payment",
    "product",
    "system_admin",
    "transaction",
]


@receiver(post_save)
def create_update_history(sender, instance, created, **kwargs):
    if sender.__module__.split(".")[0] in LIST_LABEL:
        # Just save history when instance is created or updated
        if created or not created and instance._state.adding == False:
            request = get_request()
            if request:
                user = request.user if request.user.is_authenticated else None
                company = user.company if user.company else None
            else:
                user = None
                company = None
            # get model name
            model_name = ContentType.objects.get_for_model(sender).model
            # get old data
            if not created:
                old_data = sender.objects.get(pk=instance.pk)
            else:
                old_data = None
            # save history
            history = History(
                action=History.CREATE if created else History.UPDATE,
                model_name=model_name,
                object_id=instance.pk,
                company_id=company.id if company else None,
                data={
                    "old": old_data.__str__() if old_data else None,
                    "new": instance.__str__() if instance else None,
                    "detail": model_to_dict(instance)
                    if instance
                    else model_to_dict(old_data),
                },
                user=user,
            )
            history.save()


@receiver(pre_delete)
def delete_history(sender, instance, **kwargs):
    if sender.__module__.split(".")[0] in LIST_LABEL:
        request = get_request()
        if request:
            user = request.user if request.user.is_authenticated else None
            company = user.company if user.company else None
        else:
            user = None
            company = None
        # save history
        model_name = ContentType.objects.get_for_model(sender).model
        history = History(
            action=History.DELETE,
            model_name=model_name,
            object_id=instance.pk,
            company_id=company.id if company else None,
            data={
                "old": model_to_dict(instance) if instance else None,
                "new": None,
            },
            user=user,
        )
        history.save()
