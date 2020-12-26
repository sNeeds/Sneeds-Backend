from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers


def generic_hyperlinked_related_method(parent_serializer, related_classes: list, obj,
                                       content_type_field='content_type', object_id_field='object_id'):
    for module in related_classes:
        content_type = ContentType.objects.get_for_model(module.get('model_class'))
        obj_content_type = getattr(obj, content_type_field)
        if obj_content_type == content_type:
            kwargs = {'view_name': module.get('hyperlink_view_name', None),
                      'lookup_field': module.get('hyperlink_lookup_field', None),
                      'lookup_url_kwarg': module.get('hyperlink_lookup_url_kwarg', None),
                      'format': module.get('hyperlink_format', None),
                      'read_only': True,
                      'source': object_id_field}
            serializer = serializers.HyperlinkedRelatedField(**kwargs)
            serializer.parent = parent_serializer
            return serializer.to_representation(obj)
    raise AssertionError("Wrong object or content type.")
