from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _


def generic_fk_unique_together_validator(instance, query_set, fields, *args, **kwargs):
    lookup_kwargs = {}
    for field in fields:
        lookup_kwargs[field] = getattr(instance, field)
    exists = query_set.filter(**lookup_kwargs).exists()
    if exists:
        raise ValidationError({NON_FIELD_ERRORS: _(f"The fields {fields} must make a unique set.")})