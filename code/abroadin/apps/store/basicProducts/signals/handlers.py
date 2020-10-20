from django.db.models.signals import post_save
from abroadin.apps.store.basicProducts.models import WebinarRoomLink, SoldWebinarProduct, \
    ClassRoomLink, SoldClassProduct


def post_save_sold_webinar_product(sender, instance, *args, **kwargs):
    # webinar_product = WebinarProduct.objects.get(id=instance.basic_product.id)
    WebinarRoomLink.objects.update_or_create(product=instance.webinar_product, user=instance.sold_to,
                                             defaults={})


def post_save_sold_class_product(sender, instance, *args, **kwargs):
    # class_product = ClassProduct.objects.get(id=instance.basic_product.id)
    ClassRoomLink.objects.update_or_create(product=instance.class_product, user=instance.sold_to,
                                           defaults={})


post_save.connect(post_save_sold_webinar_product, sender=SoldWebinarProduct)

post_save.connect(post_save_sold_class_product, sender=SoldClassProduct)

