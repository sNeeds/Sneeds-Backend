from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, post_save

from ..models import Cart
from ...storeBase.models import Product


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'pre_add':
        # Due to this problem products active status is validated in many to many signal
        # https://stackoverflow.com/questions/7986510/django-manytomany-model-validation
        product_qs = kwargs.get('model').objects.filter(
            id__in=list(kwargs.get('pk_set'))
        )
        if not product_qs.are_all_active():
            raise ValidationError({"products": "All products should be active."})

    elif action in ['post_add', 'post_remove', 'post_clear']:
        instance.update_price()
        instance.save()


def post_save_product(sender, instance, *args, **kwargs):
    instance.carts.all().update_price()


post_save.connect(post_save_product, sender=Product)

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)
