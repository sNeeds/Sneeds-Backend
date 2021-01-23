from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ngettext
from django.contrib.auth import get_user_model

from abroadin.apps.applyprofile.models import ApplyProfile

from .managers import ApplyProfileGroupManager
from .values import APPLY_PROFILE_PRICE_IN_DOLLAR
from ..storeBase.models import Product, SoldProduct


User = get_user_model()


class ApplyProfileGroup(Product):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apply_profiles = models.ManyToManyField(ApplyProfile)

    objects = ApplyProfileGroupManager.as_manager()

    def save(self, *args, **kwargs):
        self.real_type = ContentType.objects.get(app_label='applyprofilestore', model='applyprofilegroup')
        return super().save(*args, **kwargs)

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

    def sell(self, user, price):
        sold_apply_profile_group = SoldApplyProfileGroup.objects.create(
            sold_to=user,
            price=price
        )
        sold_apply_profile_group.apply_profiles.set(self.apply_profiles.all())

    def update_price(self):
        self.price = self.calculate_profiles_price(self.apply_profiles.all())
        self.save()

    @classmethod
    def calculate_profiles_price(cls, apply_profiles: iter):
        return len(apply_profiles) * APPLY_PROFILE_PRICE_IN_DOLLAR


class SoldApplyProfileGroup(SoldProduct):
    apply_profiles = models.ManyToManyField(ApplyProfile)

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

