from django.db.models.signals import m2m_changed, pre_save

from django.contrib.contenttypes.models import ContentType

from ..models import ApplyProfileGroup

APPLY_PROFILE_GROUP_CT = ContentType.objects.get(app_label='applyprofilestore', model='applyprofilegroup')



def m2m_changed_apply_profile_group(sender, instance, action, *args, **kwargs):
    if action == 'post_add':
        print(kwargs.get('pk_set'))


# m2m_changed.connect(m2m_changed, sender=ApplyProfileGroup.apply_profiles.through)