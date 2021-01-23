from django.db import models
from ..django.validators import generic_fk_unique_together_validator


class GenericForeignkeyUniqueTogetherValidationMixin:
    content_type_based_uniqueness_check_fields = {}

    def save(self, *args, **kwargs):
        self.validate_generic_fk_unique_together(self, *args, **kwargs)
        return super().save(*args, **kwargs)

    def validate_generic_fk_unique_together(self, *args, **kwargs):
        for ct_field_name, apps in self.content_type_based_uniqueness_check_fields.items():
            print(self.__dict__)
            try:
                content_type_obj = getattr(self, ct_field_name)
            except Exception:
                continue
            fields = apps.get(content_type_obj.app_label + '__' + content_type_obj.model, None)
            if fields:
                fields.append(str(ct_field_name))
                generic_fk_unique_together_validator(self, self.__class__.objects.all(), fields)


class CreateM2MManagerMixin:
    def create_with_m2m(self, *args, **kwargs):
        model = self.model
        model_fields = model._meta.get_fields()

        m2m_fields = {}
        for field in model_fields:
            if isinstance(field, models.ManyToManyField):
                m2m_fields[field] = kwargs.pop(field.name, [])

        print("**" , 1)
        obj = self.create(**kwargs)
        print("**" , 2)

        for field, value in m2m_fields.items():
            getattr(obj, field.name).set(value)
        print("**" , 3)
        return obj
