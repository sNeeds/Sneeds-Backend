from functools import wraps
from django.http import HttpResponseRedirect


def regular_certificate_or_none(function):
    @wraps(function)
    def wrap(self, *args, **kwargs):
        if self.is_regular_language_certificate_instance():
            return function(self, *args, **kwargs)

    return wrap
