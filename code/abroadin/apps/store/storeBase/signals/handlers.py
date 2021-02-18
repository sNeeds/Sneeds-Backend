import json

from django.db.models.signals import post_save, pre_delete, pre_save
from django.utils import timezone
from django.utils.datetime_safe import datetime

from abroadin.apps.store.carts.models import Cart
from abroadin.apps.notifications.models import SoldTimeSlotReminderEmailNotification
from abroadin.apps.store.storeBase.models import TimeSlotSale, SoldTimeSlotSale, Product
from abroadin.apps.chats.models import Chat
from abroadin.settings.config.variables import FRONTEND_URL


def pre_delete_product_receiver(sender, instance, *args, **kwargs):
    """
    When TimeSlotSale obj deletes, no signal will not trigger.
    This signal fix this problem.
    """
    Cart.objects.filter(products=instance).remove_product(instance)


def pre_save_time_slot_receiver(sender, instance, *args, **kwargs):
    consultant = instance.consultant
    if instance.price is None:
        instance.price = consultant.time_slot_price


def post_save_time_slot_sold_receiver(sender, instance, created, *args, **kwargs):
    sold_time_slot_url = FRONTEND_URL + "user/sessions/"
    start_time = instance.start_time
    end_time = instance.end_time

    data_dict = {
        "name": instance.sold_to.get_full_name(),
        "sold_time_slot_url": sold_time_slot_url,
        "start_time": str(start_time),
        "end_time": str(end_time)
    }

    if created:
        pass
        # notify_sold_time_slot.delay(
        #     send_to=instance.consultant.user.email,
        #     name=instance.consultant.user.get_full_name(),
        #     sold_time_slot_url=sold_time_slot_url,
        #     start_time=str(start_time),
        #     end_time=str(end_time)
        # )

    else:
        SoldTimeSlotReminderEmailNotification.objects.filter(sold_time_slot_id=instance.id).delete()

        # For user
        SoldTimeSlotReminderEmailNotification.objects.create(
            sold_time_slot_id=instance.id,
            send_date=datetime.now(),
            data_json=json.dumps(data_dict),
            email=instance.sold_to.email
        )

        data_dict["name"] = instance.consultant.user.get_full_name()
        # For consultant
        SoldTimeSlotReminderEmailNotification.objects.create(
            sold_time_slot_id=instance.id,
            send_date=datetime.now(),
            data_json=json.dumps(data_dict),
            email=instance.consultant.user.email
        )

    data_dict["name"] = instance.sold_to.get_full_name()
    # For user
    SoldTimeSlotReminderEmailNotification.objects.create(
        sold_time_slot_id=instance.id,
        send_date=instance.start_time - timezone.timedelta(days=1),
        data_json=json.dumps(data_dict),
        email=instance.sold_to.email
    )
    SoldTimeSlotReminderEmailNotification.objects.create(
        sold_time_slot_id=instance.id,
        send_date=instance.start_time - timezone.timedelta(hours=2),
        data_json=json.dumps(data_dict),
        email=instance.sold_to.email
    )

    data_dict["name"] = instance.consultant.user.get_full_name()
    # For consultant
    SoldTimeSlotReminderEmailNotification.objects.create(
        sold_time_slot_id=instance.id,
        send_date=instance.start_time - timezone.timedelta(days=1),
        data_json=json.dumps(data_dict),
        email=instance.consultant.user.email
    )
    SoldTimeSlotReminderEmailNotification.objects.create(
        sold_time_slot_id=instance.id,
        send_date=instance.start_time - timezone.timedelta(hours=2),
        data_json=json.dumps(data_dict),
        email=instance.consultant.user.email
    )


def post_save_product_receiver(sender, instance, *args, **kwargs):
    cart_qs = Cart.objects.filter(products__in=[instance])

    # Used when time slot sold price is changed and its signal is triggered to
    # update this model or product set active to False
    for obj in cart_qs:
        obj.update_products()
        obj.update_price()


def create_chat(sender, instance, *args, **kwargs):
    user = instance.sold_to
    consultant = instance.consultant
    if not Chat.objects.filter(user=user, consultant=consultant).exists():
        Chat.objects.create(user=user, consultant=consultant)


pre_save.connect(pre_save_time_slot_receiver, sender=TimeSlotSale)

post_save.connect(post_save_product_receiver, sender=Product)
# Signal is not fired when subclasses were updated.
# https://stackoverflow.com/questions/14758250/django-post-save-signal-on-parent-class-with-multi-table-inheritance
for subclass in Product.__subclasses__():
    post_save.connect(post_save_product_receiver, subclass)

post_save.connect(post_save_time_slot_sold_receiver, sender=SoldTimeSlotSale)
post_save.connect(create_chat, sender=SoldTimeSlotSale)

pre_delete.connect(pre_delete_product_receiver, sender=Product)
