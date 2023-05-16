# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import YourModel
# from .utils import compress_image

# @receiver(post_save, sender=YourModel)
# def optimize_image(sender, instance, created, **kwargs):
#     if created:
#         file = instance.image.file
#         compress_image(file)