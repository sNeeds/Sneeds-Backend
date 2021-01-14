from django.db.models.signals import m2m_changed, pre_save

from django.contrib.contenttypes.models import ContentType

APPLY_PROFILE_GROUP_CT = ContentType.objects.get(app_label='applyprofilestore', model='applyprofilegroup')


def pre_save_apply_profile_group(instance, sender, *args, **kwargs):
    instance.real_type = APPLY_PROFILE_GROUP_CT


