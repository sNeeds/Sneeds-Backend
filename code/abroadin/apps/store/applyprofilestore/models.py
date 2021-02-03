from django.db import models, transaction
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

    @property
    def title(self):
        return f'Similar Students'

    @property
    def subtitle(self):
        apply_profiles_count = self.apply_profiles.all().count()
        msg = ngettext(
            '%(count)d Profile',
            '%(count)d Profiles',
            apply_profiles_count,
        ) % {
                  'count': apply_profiles_count,
              }

        return msg

    @transaction.atomic
    def sell(self):
        sold_apply_profile_group = SoldApplyProfileGroup.objects.create(
            sold_to=self.user,
            price=self.price
        )
        sold_apply_profile_group.apply_profiles.set(self.apply_profiles.all())
        super().sell()

    def update_price(self):
        self.price = self.calculate_profiles_price(self.apply_profiles.all())
        self.save()

    @classmethod
    def calculate_profiles_price(cls, apply_profiles: iter):
        discount = 1
        if len(apply_profiles) != 1:
            discount = 0.7
        return int((len(apply_profiles) * APPLY_PROFILE_PRICE_IN_DOLLAR * discount) / 1000) * 1000

    @property
    def normal_price(self):
        return int((len(self.apply_profiles.all()) * APPLY_PROFILE_PRICE_IN_DOLLAR) / 1000) * 1000


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
