from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ngettext
from django.contrib.auth import get_user_model

from .managers import ApplyProfileGroupManager
from ..storeBase.models import Product

from abroadin.apps.applyprofile.models import ApplyProfile

User = get_user_model()

APPLY_PROFILE_GROUP_CT = ContentType.objects.get(app_label='applyprofilestore', model='applyprofilegroup')


class ApplyProfileGroup(Product):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    user = models.ForeignKey(to=User,
                             null=True,
                             blank=True,
                             on_delete=models.SET_NULL
                             )

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

    @classmethod
    def user_bought_apply_profiles(cls, user):
        cls.objects.filter(user=user, )
