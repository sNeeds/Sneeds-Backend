from django.core.exceptions import FieldDoesNotExist
from django.db.models.constants import LOOKUP_SEP
from django.contrib.admin.utils import get_fields_from_path, _get_non_gfk_field, FieldIsAForeignKeyColumnName, \
    get_model_from_relation


def lookup_field(name, obj, model_admin=None):
    opts = obj._meta
    try:
        f = _get_non_gfk_field(opts, name)
    except (FieldDoesNotExist, FieldIsAForeignKeyColumnName):
        # For non-field values, the value is either a method, property or
        # returned via a callable.
        if callable(name):
            attr = name
            value = attr(obj)
        elif hasattr(model_admin, name) and name != '__str__':
            attr = getattr(model_admin, name)
            value = attr(obj)
        else:
            attr = getattr(obj, name)
            if callable(attr):
                value = attr()
            else:
                value = attr
        f = None
    else:
        attr = None
        value = getattr(obj, name)
    return f, attr, value


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
