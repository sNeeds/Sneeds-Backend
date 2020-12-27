from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

# For prevent creating HyperlinkedRelatedField every time method is called
MODEL_CLASS_HYPERLINKED_FIELDS = {}


def _create_hyperlinked_field(parent_serializer, module, object_id_field):
    kwargs = {'view_name': module.get('hyperlink_view_name', None),
              'lookup_field': module.get('hyperlink_lookup_field', None),
              'lookup_url_kwarg': module.get('hyperlink_lookup_url_kwarg', None),
              'format': module.get('hyperlink_format', None),
              'read_only': True,
              'source': object_id_field,
              }
    serializer = serializers.HyperlinkedRelatedField(**kwargs)
    serializer.parent = parent_serializer
    return serializer


def generic_hyperlinked_related_method(parent_serializer, related_classes: list, obj,
                                       content_type_field='content_type', object_id_field='object_id'):
    for module in related_classes:
        model_content_type = ContentType.objects.get_for_model(module.get('model_class'))
        obj_content_type = getattr(obj, content_type_field)
        if obj_content_type == model_content_type:
            key = "{}-{}-{}".format(str(parent_serializer.__class__), str(module.get('model_class')),
                                    module.get('view_name'))
            serializer = MODEL_CLASS_HYPERLINKED_FIELDS.get(key, None)
            if serializer is None:
                serializer = _create_hyperlinked_field(parent_serializer, module, object_id_field)
                MODEL_CLASS_HYPERLINKED_FIELDS[key] = serializer

            return serializer.to_representation(obj)
    raise AssertionError("Wrong object or content type.")

