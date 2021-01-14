from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .VALUES import MAX_ALLOWED_APPLY_PROFILES


def validate_apply_profiles(apply_profiles):
    if len(apply_profiles) > MAX_ALLOWED_APPLY_PROFILES:
        ValidationError({'apply_profiles': _('apply_profiles count violates the maximum allowed constraint.')})

    return apply_profiles
