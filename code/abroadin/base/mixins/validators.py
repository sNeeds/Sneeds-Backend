from django.db import models
from ..django.validators import generic_fk_unique_together_validator


class GenericForeignkeyUniqueTogetherValidationMixin:
    content_type_based_uniqueness_check_fields = {}

    def validate_unique(self, exclude=None):
        for ct_field_name, apps in self.content_type_based_uniqueness_check_fields.items():
            try:
                content_type_obj = getattr(self, ct_field_name)
            except Exception:
                continue
            fields = apps.get(content_type_obj.app_label + '__' + content_type_obj.model, None)
            if fields:
                fields.append(str(ct_field_name))
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
