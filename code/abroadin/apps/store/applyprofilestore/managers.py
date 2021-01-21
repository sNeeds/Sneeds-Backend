from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from .validators import validate_apply_profiles
from .values import APPLY_PROFILE_PRICE_IN_DOLLAR


class ApplyProfileGroupManager(QuerySet):

    def create_by_apply_profiles(self, **kwargs):
        apply_profiles = kwargs.pop('apply_profiles')
        try:
            apply_profiles = validate_apply_profiles(apply_profiles)
        except Exception as e:
            raise ValidationError({'apply_profiles': _(e.message)})

        obj = self.create(**kwargs, price=APPLY_PROFILE_PRICE_IN_DOLLAR)
        obj.apply_profiles.set(apply_profiles)
        obj.update_price()
        return obj
