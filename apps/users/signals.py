from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import User, Wishlist
from apps.shop.models import Order


@receiver(post_save, sender=User)
def after_user_created(sender, **kwargs):
    print('in signal')
    user = kwargs.get('instance')
    if kwargs.get('created'):
        Wishlist.objects.create(user=user)
        Order.objects.create(user=user)
