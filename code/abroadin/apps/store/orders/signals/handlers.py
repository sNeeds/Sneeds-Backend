from django.db.models.signals import post_save, pre_save

from ..models import Order
from ..utils import unique_order_id_generator
from abroadin.settings.config.variables import FRONTEND_URL


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


def post_save_send_order_created(sender, instance, created, *args, **kwargs):
    order_url = FRONTEND_URL + "user/orders/" + str(instance.id)


pre_save.connect(pre_save_create_order_id, sender=Order)
post_save.connect(post_save_send_order_created, sender=Order)


