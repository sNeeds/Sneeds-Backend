from ..django.validators import generic_fk_unique_together_validator


class GenericForeignkeyUniqueTogetherValidationMixin:
    # content_type_fields = {
    #     'content_type_field1_name': {
    #         'app_model1': {
    #             'check_fields': ['object_id', 'active']
    #         },
    #         'app_model2': {
    #             'fields': ['object_id', 'type', 'score']
    #         },
    #     },
    #     'content_type_field2_name': {
    #         'app_model3': {
    #             'fields': ['object_id', 'active', 'type']
    #         }
    #     }
    # }

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
            fields = apps.get(content_type_obj.app_label+'__'+content_type_obj.model, None)
            if fields:
                fields.append(str(ct_field_name))
                generic_fk_unique_together_validator(self, self.__class__.objects.all(), fields)
