import json
from enumfields import Enum, EnumField
from django.conf import settings


# https://stackoverflow.com/questions/21631878/celery-is-there-a-way-to-write-custom-json-encoder-decoder
class CEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return {
                '__type__': '__enum__',
                'name': obj.name,
                'enum_class': obj.__class__.__name__,
            }
        else:
            return json.JSONEncoder.default(self, obj)


def c_decoder(obj):
    if '__type__' in obj:
        if obj['__type__'] == '__enum__':
            return settings.ENUM_CLASSES.get(obj['enum_class'])[obj['name']]
    return obj


# Encoder function
def c_dumps(obj):
    return json.dumps(obj, cls=CEncoder)


# Decoder function
def c_loads(obj):
    return json.loads(obj, object_hook=c_decoder)
