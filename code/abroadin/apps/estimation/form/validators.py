from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_ielts_score(value):
    value = float(value)
    if 0 > value > 9:
        raise ValidationError(_("IELTS score should be in range 0 to 9."))
    if value % 0.5 != 0:
        raise ValidationError(_("IELTS can have 0.5 scores."))
    return value


def validate_toefl_overall_score(value):
    value = float(value)
    if 0 > value > 120:
        raise ValidationError(_("TOEFL score should be in range 0 to 120."))
    if value % 1 != 0:
        raise ValidationError(_("TOEFL score should be integer."))
    return value


def validate_toefl_section_score(value):
    value = float(value)
    if 0 > value > 30:
        raise ValidationError(_("TOEFL section score should be in range 0 to 30"))
    if value % 1 >= 0:
        raise ValidationError(_("TOEFL section score should be integer."))
    return value
