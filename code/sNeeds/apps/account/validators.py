from django.core.exceptions import ValidationError
import os

from django.utils.translation import gettext_lazy as _

from enumfields import Enum


class LanguageCertificateType(Enum):
    """Every time updated this class in this file update the mirror class in account.models"""

    IELTS = 'IELTS'
    TOEFL = 'TOEFL'
    GMAT = 'GMAT'
    GRE_GENERAL = 'GRE General'
    GRE_CHEMISTRY = 'GRE Chemistry'
    GRE_MATHEMATICS = 'GRE Mathematics'
    GRE_LITERATURE = 'GRE Literature'
    GRE_BIOLOGY = 'GRE Biology'
    GRE_PHYSICS = 'GRE Physics'
    GRE_PSYCHOLOGY = 'GRE Psychology'
    DUOLINGO = 'Duolingo'


def validate_marital_status(value):
    pass


def validate_grade(value):
    pass


def validate_apply_grade(value):
    pass


def validate_language_certificate(value):
    pass


def validate_mainland(value):
    pass


def validate_resume_file_extension(value):
    ext = ""
    if os.path.splitext(value.name)[1] is not None:
        ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
    return value


def validate_resume_file_size(value):
    filesize = value.size

    if filesize > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    else:
        return value


def ten_factor_validator(value):
    if value % 10 != 0:
        raise ValidationError("Value Should be a factor of 10")
    else:
        return value


def regular_certificate_type_validator(value):
    print(value)
    if value not in [LanguageCertificateType.IELTS, LanguageCertificateType.TOEFL]:
        raise ValidationError(_("Value is not in allowed certificate types."))
    return value


def gmat_certificate_type_validator(value):
    if value not in [LanguageCertificateType.GMAT]:
        raise ValidationError(_("Value is not in allowed certificate types."))
    return value


def gre_general_certificate_type_validator(value):
    if value not in [LanguageCertificateType.GRE_GENERAL]:
        raise ValidationError(_("Value is not in allowed certificate types."))
    return value


def gre_subject_certificate_type_validator(value):
    if value not in [LanguageCertificateType.GRE_CHEMISTRY, LanguageCertificateType.GRE_LITERATURE,
                     LanguageCertificateType.GRE_MATHEMATICS]:
        raise ValidationError(_("Value is not in allowed certificate types."))
    return value


def gre_biology_certificate_type_validator(value):
    if value not in [LanguageCertificateType.GRE_BIOLOGY]:
        raise ValidationError(_("Value is not in allowed certificate types."))
    return value


def gre_physics_certificate_type_validator(value):
    if value not in [LanguageCertificateType.GRE_PHYSICS]:
        raise ValidationError(_("Value is not in allowed certificate types."))
    return value


def gre_psychology_certificate_type_validator(value):
    if value not in [LanguageCertificateType.GRE_PSYCHOLOGY]:
        raise ValidationError(_("Value is not in allowed certificate types."))
    return value


def duolingo_certificate_type_validator(value):
    if value not in [LanguageCertificateType.DUOLINGO]:
        raise ValidationError(_("Value is not in allowed certificate types."))
    return value
