from django.db.models.signals import pre_save, pre_delete
from django.core.cache import cache
from django.dispatch import receiver
from .models import Category


@receiver([pre_delete, pre_save], sender=Category)
def pre_delete_receiver_category(sender, instance, *args, **kwargs):
    cache.delete('category-list')
