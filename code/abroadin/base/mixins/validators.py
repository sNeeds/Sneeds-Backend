from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import gettext as _


class GenericForeignkeyUniqueTogetherValidationMixin:
    def _get_content_type_obj(self, field_name):
        try:
            content_type_obj = getattr(self, field_name)
        except AttributeError:
            raise AttributeError(
                f"The {field_name} field name is not a valid  field "
                f"name for {self.__class__.__name__} model."
            )
        if not isinstance(content_type_obj, ContentType):
            raise AttributeError(
                f"The {field_name} field name is not a ContentType instance "
                f"for {self.__class__.__name__} model."
            )
        return content_type_obj

    def _generic_fk_unique_together_validator(self, fields):
        lookup_kwargs = {}
        for field in fields:
            lookup_kwargs[field] = getattr(self, field)

        model_class = self.__class__
        qs = model_class._default_manager.filter(**lookup_kwargs)

        model_class_pk = self._get_pk_val(model_class._meta)
        if not self._state.adding and model_class_pk is not None:
            qs = qs.exclude(pk=model_class_pk)

        if qs.exists():
            raise ValidationError(
                {NON_FIELD_ERRORS: _(f"The fields {fields} must make a unique set.")}
            )

    def validate_unique(self, exclude=None):
        for ct_field_name, apps in self.content_type_uniqueness_check.items():
            ct_obj = self._get_content_type_obj(ct_field_name)
            fields = apps.get(ct_obj.app_label + '__' + ct_obj.model, None)
            if fields:
                self._generic_fk_unique_together_validator([ct_field_name] + fields)

        return super().validate_unique(exclude)


class CreateM2MManagerMixin:
    def create_with_m2m(self, *args, **kwargs):
        model = self.model
        model_fields = model._meta.get_fields()

        m2m_fields = {}
        for field in model_fields:
            if isinstance(field, models.ManyToManyField):
                m2m_fields[field] = kwargs.pop(field.name, [])

        obj = self.create(**kwargs)

        for field, value in m2m_fields.items():
            getattr(obj, field.name).set(value)

        return obj
