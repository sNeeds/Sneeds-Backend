from django.db.models.signals import post_save, pre_delete

from abroadin.apps.store.carts.models import Cart
from abroadin.apps.store.storeBase.models import Product


def pre_delete_product_receiver(sender, instance, *args, **kwargs):
    """
    When TimeSlotSale obj deletes, no signal will not trigger.
    This signal fix this problem.
    """
    Cart.objects.filter(products=instance).remove_product(instance)


def post_save_product_receiver(sender, instance, *args, **kwargs):
    cart_qs = Cart.objects.filter(products__in=[instance])

    # Used when time slot sold price is changed and its signal is triggered to
    # update this model or product set active to False
    for obj in cart_qs:
        obj.update_products()
        obj.update_price()


post_save.connect(post_save_product_receiver, sender=Product)
# Signal is not fired when subclasses were updated.
# https://stackoverflow.com/questions/14758250/django-post-save-signal-on-parent-class-with-multi-table-inheritance
for subclass in Product.__subclasses__():
    post_save.connect(post_save_product_receiver, subclass)

pre_delete.connect(pre_delete_product_receiver, sender=Product)
