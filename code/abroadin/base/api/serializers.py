from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

# For prevent creating HyperlinkedRelatedField every time method is called
MODEL_CLASS_HYPERLINKED_FIELDS = {}


def _create_hyperlinked_field(parent_serializer, related_class, object_id_field):
    kwargs = {'view_name': related_class.get('hyperlink_view_name', None),
              'lookup_field': related_class.get('hyperlink_lookup_field', None),
              'lookup_url_kwarg': related_class.get('hyperlink_lookup_url_kwarg', None),
              'format': related_class.get('hyperlink_format', None),
              'read_only': True,
              'source': object_id_field,
              }
    serializer = serializers.HyperlinkedRelatedField(**kwargs)
    serializer.parent = parent_serializer
    return serializer


def generic_hyperlinked_related_method(parent_serializer, related_classes: list, obj,
                                       content_type_field='content_type', object_id_field='object_id'):
    """
    Sample right definition of related_classes
    related_classes = [
        {
            'model_class': ApplyProfile,
            'hyperlink_view_name': 'applyprofile:apply-profile-detail',
            'hyperlink_lookup_field': 'object_id',
            'hyperlink_lookup_url_kwarg': 'id',
            'hyperlink_format': None
        },
    ]
    """

    for related_class in related_classes:
        model_content_type = ContentType.objects.get_for_model(related_class.get('model_class'))
        obj_content_type = getattr(obj, content_type_field)
        if obj_content_type == model_content_type:
            key = "{}-{}-{}".format(str(parent_serializer.__class__), str(related_class.get('model_class')),
                                    related_class.get('view_name'))
            serializer = MODEL_CLASS_HYPERLINKED_FIELDS.get(key, None)
            if serializer is None:
                serializer = _create_hyperlinked_field(parent_serializer, related_class, object_id_field)
                MODEL_CLASS_HYPERLINKED_FIELDS[key] = serializer

            print(serializer)
            print(obj)

            d = serializer.to_representation(obj)
            print('d', d)
            return d
    raise AssertionError("Wrong object or content type.")

