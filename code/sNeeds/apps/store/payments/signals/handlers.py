from django.db.models.signals import pre_save

from ..models import ConsultantDepositInfo
from sNeeds.apps.store.payments.utils import unique_consultant_deposit_info_id_generator


def pre_save_create_consultant_deposit_info_id(sender, instance, *args, **kwargs):
    if not instance.consultant_deposit_info_id:
        instance.consultant_deposit_info_id = unique_consultant_deposit_info_id_generator(instance)


pre_save.connect(pre_save_create_consultant_deposit_info_id, sender=ConsultantDepositInfo)
