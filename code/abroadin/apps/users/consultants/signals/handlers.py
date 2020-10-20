from django.db.models.signals import post_save

from abroadin.apps.users.consultants.models import ConsultantProfile
from abroadin.apps.store.storeBase.models import TimeSlotSale


def post_save_consultant(sender, instance, *args, **kwargs):
    time_slots_qs = TimeSlotSale.objects.filter(consultant=instance)
    time_slots_qs.update(price=instance.time_slot_price)


post_save.connect(post_save_consultant, sender=ConsultantProfile)
