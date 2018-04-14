from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Recipe


@receiver(pre_save, sender=Recipe)
def set_lower_case_name(sender, instance, *args, **kwargs):
    instance.name = instance.name.lower()