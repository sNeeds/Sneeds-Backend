from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

a = [
    {
        'model_class': serializers.ModelSerializer,
        'representation_identifier': '',
        'pk_field': 'id',
        'pk': 2,
        'primary_key_related_field': serializers.PrimaryKeyRelatedField()
        'query_set': '',
        'hyperlinked_serializer': serializers.CharField,
    }
]


class ContentTypeRelatedField(serializers.RelatedField):
    def __init__(self, **kwargs):
        self.related_classes = kwargs.pop('related_classes', None)
        assert self.related_classes is not None, _("related_classes may not be None.")
        assert isinstance(self.related_classes, list), _("related classes should be an object of list")
        # assert len(related_classes) > 0 , _('related_classes ')
        for module in self.related_classes:
            assert 'model_class' in module and 'pk_field' in module, \
                _('Not enough info in related_classes. Read class doc')

    # def get_queryset(self):
    #     return ContentType.objects.filter(app_label='storePackages', model='soldstorepaidpackagephase') | \
    #            ContentType.objects.filter(app_label='storePackages', model='soldstoreunpaidpackagephase')

    def to_internal_value(self, data):
        representation_identifier = data.get('representation_identifier')
        for module in self.related_classes:
            if representation_identifier == module.get('representation_identifier'):
                # if module.get('pk_field') is not None:
                #     data = self.pk_field.to_internal_value(data)
                # try:
                #     return self.get_queryset().get(pk=data)
                # except ObjectDoesNotExist:
                #     self.fail('does_not_exist', pk_value=data)
                # except (TypeError, ValueError):
                #     self.fail('incorrect_type', data_type=type(data).__name__)
        else:
            raise serializers.ValidationError({"content_type": "ContentTypeRelatedField wrong instance."}, code=400)

    def to_representation(self, value):
        print('ASDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
        # print(value)
        for module in self.related_classes:
            if isinstance(value, module.get('model_class')):
                print(module.get('model_class'))
                return {
                    'representation_identifier': module.get('representation_identifier'),
                    'model_class': module.get('model_class'),
                    'object_pk': value.pk
                }

        raise serializers.ValidationError({"content_type": "ContentTypeRelatedField wrong instance."}, code=400)
