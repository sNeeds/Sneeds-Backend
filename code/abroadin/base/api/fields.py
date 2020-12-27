from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


from rest_framework.exceptions import ValidationError

APP_MODEL_SEPARATOR = '__'


def _get_content_type_identifier(content_type: ContentType) -> str:
    return content_type.app_label + APP_MODEL_SEPARATOR + content_type.model


def _get_content_type_by_identifier(identifier: str) -> tuple:
    t = identifier.split(APP_MODEL_SEPARATOR)
    if len(t) > 2:
        raise ValidationError('Wrong identifier')
    return t[0], t[1]


# a = [
#     {
#         'model_class': serializers.ModelSerializer,
#         'representation_identifier': '',
#         'pk_field': 'id',
#         'pk': 2,
#         'primary_key_related_field': serializers.PrimaryKeyRelatedField(),
#         'query_set': '',
#         'hyperlinked_related_field': serializers.HyperlinkedRelatedField(),
#     }
# ]

class GenericRelatedField(serializers.RelatedField):
    def __init__(self, **kwargs):
        self.related_classes = kwargs.pop('related_classes', None)
        # print('related classes', self.related_classes)
        assert self.related_classes is not None, _("related_classes may not be None.")
        assert isinstance(self.related_classes, list), _("related classes should be an object of list")
        for module in self.related_classes:
            assert 'model_class' in module and 'primary_key_related_field' in module, \
                _('Not enough info in related_classes. Read class doc')

        self.queryset = [1]
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        print('to_internalll', data)
        app_label, model = _get_content_type_by_identifier(data.get('representation_identifier'))
        content_type = ContentType.objects.get(app_label=app_label, model=model)
        pk = data.get('pk')
        for module in self.related_classes:
            if module.get('model_class') == content_type.model_class():
                return module.get('primary_key_related_field').to_internal_value(pk)
        raise serializers.ValidationError({"content_type": "ContentTypeRelatedField wrong instance."}, code=400)

    def to_representation(self, value):
        print('to_representation')
        # print(value)
        if isinstance(value, int):
            return value
        for module in self.related_classes:
            if isinstance(value, module.get('model_class')):
                content_type = ContentType.objects.get_for_model(module.get('model_class'))
                print(module.get('model_class'))
                return {
                    'representation_identifier': _get_content_type_identifier(content_type),
                    'pk': value.pk,
                    # 'url': module.get('hyperlinked_related_field').to_representation(value)
                }

        raise AssertionError("ContentTypeRelatedField wrong instance.")


class ContentTypeRelatedField(serializers.RelatedField):
    allowed_content_types = None

    def __init__(self, **kwargs):
        self.related_classes = kwargs.pop('related_classes', None)
        assert self.related_classes is not None, _("related_classes may not be None.")
        assert isinstance(self.related_classes, list), _("related classes should be an object of list")

        self.queryset = self.perform_query_set()
        self.allowed_content_types = self.perform_allowed_content_types()
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if data not in self.allowed_content_types:
            raise serializers.ValidationError({"content_type": "ContentTypeRelatedField wrong instance."}, code=400)
        app_label, model = _get_content_type_by_identifier(data)
        return ContentType.objects.get(app_label=app_label, model=model)

    def to_representation(self, value):
        ret = _get_content_type_identifier(value)
        assert ret in self.allowed_content_types, _("Object is not allowed to be serialized through this"
                                                    " related serializer")
        return ret
        # raise serializers.ValidationError({"content_type": "ContentTypeRelatedField wrong instance."}, code=400)

    def perform_query_set(self):
        query_set = ContentType.objects.none()

        for module in self.related_classes:
            content_type = ContentType.objects.get_for_model(model=module['model_class'])
            query_set |= ContentType.objects.filter(app_label=content_type.app_label, model=content_type.model)
        return query_set

    def perform_allowed_content_types(self):
        return [_get_content_type_identifier(ContentType.objects.get_for_model(module['model_class']))
                for module in self.related_classes]


# h =[
#     (ApplyProfile, serializers.HyperlinkedRelatedField())
# ]


class GenericHyperlinkedRelatedField(serializers.RelatedField):

    def __init__(self, **kwargs):
        self.read_only = True
        self.related_classes = kwargs.pop('related_classes', None)
        assert self.related_classes is not None, _("related_classes may not be None.")
        assert isinstance(self.related_classes, list), _("related classes should be an object of list")

        self.queryset = self.perform_query_set()
        self.allowed_content_types = self.perform_allowed_content_types()
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        for module in self.related_classes:
            if isinstance(value, module[0]):
                return module[1].to_representaion()

    def perform_query_set(self):
        query_set = ContentType.objects.none()

        for module in self.related_classes:
            content_type = ContentType.objects.get_for_model(model=module[0])
            query_set |= ContentType.objects.filter(app_label=content_type.app_label, model=content_type.model)
        return query_set

    def perform_allowed_content_types(self):
        return [_get_content_type_identifier(ContentType.objects.get_for_model(module[0])) for module in self.related_classes]