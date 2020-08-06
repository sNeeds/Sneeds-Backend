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






