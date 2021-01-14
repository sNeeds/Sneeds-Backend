from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ngettext

from .managers import ApplyProfileGroupManager
from ..storeBase.models import Product

from abroadin.apps.applyprofile.models import ApplyProfile

APPLY_PROFILE_GROUP_CT = ContentType.objects.get(app_label='applyprofilestore', model='applyprofilegroup')


class ApplyProfileGroup(Product):
    apply_profiles = models.ManyToManyField(ApplyProfile)

    objects = ApplyProfileGroupManager.as_manager()

    @property
    def title(self):
        return f'Similar admissions'

    @property
    def subtitle(self):
        apply_profiles_count = self.apply_profiles.all().count()
        msg = ngettext(
            '%(count)d Student Profile',
            '%(count)d Student Profiles',
            apply_profiles_count,
        ) % {
                   'count': apply_profiles_count,
               }

        return msg


class SoldApplyProfileGroup(Product):
    apply_profiles = models.ManyToManyField(ApplyProfile)

    # def save(self, *args, **kwargs):
    #     self.real_type =

    def title(self):
        return f'Similar admissions'

    def subtitle(self):
        apply_profiles_count = self.apply_profiles.all().count()
        msg = ngettext(
            '%(count)d Student Profile',
            '%(count)d Student Profiles',
            apply_profiles_count,
        ) % {
                  'count': apply_profiles_count,
              }

        return msg
