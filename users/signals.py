from django.core.cache import cache
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, pre_delete

User = get_user_model()


@receiver([pre_save, pre_delete], sender=User)
def pre_delete_receiver_product(sender, instance, *args, **kwargs):
    cache.delete('user-list')
