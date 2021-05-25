from .utils import unique_slug_generator
from django.db.models.signals import pre_save, post_delete, pre_delete
from django.core.cache import cache
from django.dispatch import receiver
from .models import Product, Category


@receiver(pre_save, sender=Product)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    cache.delete('product-list')


@receiver(pre_delete, sender=Product)
def pre_delete_receiver_product(sender, instance, *args, **kwargs):
    cache.delete('product-list')


@receiver([pre_delete, pre_save], sender=Category)
def pre_delete_receiver_category(sender, instance, *args, **kwargs):
    cache.delete('category-list')
