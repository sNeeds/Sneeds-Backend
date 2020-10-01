import six
from rest_framework import serializers


class EnumField(serializers.ChoiceField):
    def __init__(self, enum, **kwargs):
        self.enum = enum
        kwargs['choices'] = [(e.name, e.name) for e in enum]
        super(EnumField, self).__init__(**kwargs)

    def to_representation(self, obj):
        if hasattr(obj, 'name'):
            return obj.name
        else:
            return self.choice_strings_to_values.get(six.text_type(obj), obj)

    def to_internal_value(self, data):
        try:
            return self.enum[data]
        except KeyError:
            self.fail('invalid_choice', input=data)


class CustomRepresentation:
    def __init__(self, value, name):
        self.value = value
        self.name = name

    def __str__(self):
        return self.name

