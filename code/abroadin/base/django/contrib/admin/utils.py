from django.core.exceptions import FieldDoesNotExist
from django.db.models.constants import LOOKUP_SEP
from django.contrib.admin.utils import  lookup_field


def lookup_field_support_nested(name, obj, model_admin=None):
    if not callable(name):
        pieces = name.split(LOOKUP_SEP)
        value = obj
        for piece in pieces:
            f, attr, value = lookup_field(piece, value, model_admin)

            if value is None:
                break

        return f, attr, value

    else:
        return lookup_field(name, obj, model_admin)
