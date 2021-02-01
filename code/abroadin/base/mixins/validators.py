from django.contrib.contenttypes.models import ContentType
from django.db import models
from ..django.validators import generic_fk_unique_together_validator


class GenericForeignkeyUniqueTogetherValidationMixin:
    content_type_uniqueness_check = {}

    def _get_content_type_obj(self, field_name):
        try:
            content_type_obj = getattr(self, field_name)
        except AttributeError:
            raise AttributeError(
                f"The {field_name} field name is not a valid content type field "
                f"name for {self.__class__.__name__} model."
            )
        if not isinstance(content_type_obj, ContentType):
            raise AttributeError(
                f"The {field_name} field name is not a ContentType instance "
                f"for {self.__class__.__name__} model."
            )

        return content_type_obj

    def validate_unique(self, exclude=None):
        for ct_field_name, apps in self.content_type_uniqueness_check.items():
            ct_obj = self._get_content_type_obj(ct_field_name)
            fields = apps.get(ct_obj.app_label + '__' + ct_obj.model.__name__, None)
            if fields:
                fields.insert(0, str(ct_field_name))
                generic_fk_unique_together_validator(self, self.__class__.objects.all(), fields)
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
