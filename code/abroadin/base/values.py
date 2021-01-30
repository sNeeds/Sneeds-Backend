from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class AccessibilityTypeChoices(TextChoices):
    PARTIAL = 'Partial', _('Partial')
    LOCKED = 'Locked', _('Locked')
    UNLOCKED = 'Unlocked', _('Unlocked')

