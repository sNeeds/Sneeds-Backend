from django.db.models.signals import post_save, post_delete

from sNeeds.apps.store.videochats.models import Room
from sNeeds.apps.store.videochats.utils import delete_room
from sNeeds.apps.store.videochats.tasks import create_room_with_users_in_skyroom, delete_room


def post_save_room_receiver(sender, instance, created, *args, **kwargs):
    if created:
        instance.sold_time_slot.used = True
        instance.sold_time_slot.save()

        create_room_with_users_in_skyroom.delay(instance.id)


def post_delete_room_receiver(sender, instance, *args, **kwargs):
    delete_room.delay(instance.room_id)


post_save.connect(post_save_room_receiver, sender=Room)
post_delete.connect(post_delete_room_receiver, sender=Room)
