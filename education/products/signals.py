from django.dispatch import Signal, receiver
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from products.models import Group
from products.utils import distribute_users_to_groups

access_granted = Signal()


@receiver(access_granted)
def on_access_granted(sender, product, **kwargs):
    try:
        if product.start_date > timezone.now():
            distribute_users_to_groups(product)
    except Group.DoesNotExist:
        raise ValidationError("Все группы заполнены.")
