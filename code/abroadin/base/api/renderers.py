import base64
from collections import OrderedDict
from urllib import parse

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Page
from django.http.multipartparser import parse_header
from django.template import engines, loader
from django.urls import NoReverseMatch
from django.utils.html import mark_safe

from rest_framework import VERSION, exceptions, serializers, status
from rest_framework.compat import (
    INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS, coreapi, coreschema,
    pygments_css, yaml
)
from rest_framework.exceptions import ParseError
from rest_framework.request import is_form_media_type, override_method
from rest_framework.settings import api_settings
from rest_framework.utils import encoders, json
from rest_framework.utils.breadcrumbs import get_breadcrumbs
from rest_framework.utils.field_mapping import ClassLookupDict


from rest_framework import renderers


class BrowsableAPIRenderer(renderers.BrowsableAPIRenderer):

    def get_rendered_html_form(self, data, view, method, request):
        """
        Return a string representing a rendered HTML form, possibly bound to
        either the input or output data.

        In the absence of the View having an associated form then return None.
        """
        # See issue #2089 for refactoring this.
        serializer = getattr(data, 'serializer', None)
        if serializer and not getattr(serializer, 'many', False):
            instance = getattr(serializer, 'instance', None)
            if isinstance(instance, Page):
                instance = None
        else:
            instance = None

        # If this is valid serializer data, and the form is for the same
        # HTTP method as was used in the request then use the existing
        # serializer instance, rather than dynamically creating a new one.
        if request.method == method and serializer is not None:
            try:
                kwargs = {'data': request.data}
            except ParseError:
                kwargs = {}
            existing_serializer = serializer
        else:
            kwargs = {}
            existing_serializer = None

        with override_method(view, request, method) as request:
            if not self.show_form_for_method(view, method, request, instance):
                return

            if method in ('DELETE', 'OPTIONS'):
                return True  # Don't actually need to return a form

            has_serializer = getattr(view, 'get_serializer', None)
            has_serializer_class = getattr(view, 'serializer_class', None)

            if (
                    (not has_serializer and not has_serializer_class) or
                    not any(is_form_media_type(parser.media_type) for parser in view.parser_classes)
            ):
                return

            if existing_serializer is not None:
                try:
                    return self.render_form_for_serializer(existing_serializer)
                except TypeError:
                    pass

            if has_serializer:
                if method in ('PUT', 'PATCH'):
                    if hasattr(view, 'get_request_serializer'):
                        serializer = view.get_request_serializer(instance=instance, **kwargs)
                    else:
                        serializer = view.get_serializer(instance=instance, **kwargs)
                else:
                    if hasattr(view, 'get_request_serializer'):
                        serializer = view.get_request_serializer(**kwargs)
                    else:
                        serializer = view.get_serializer(**kwargs)
            else:
                # at this point we must have a serializer_class
                if method in ('PUT', 'PATCH'):
                    if hasattr(view, 'get_request_serializer_class'):
                        serializer = self._get_serializer(view.get_request_serializer_class(), view,
                                                          request, instance=instance, **kwargs)
                    else:
                        serializer = self._get_serializer(view.serializer_class, view,
                                                          request, instance=instance, **kwargs)
                else:
                    if hasattr(view, 'get_request_serializer_class'):
                        serializer = self._get_serializer(view.get_request_serializer_class(), view,
                                                          request, **kwargs)
                    else:
                        serializer = self._get_serializer(view.serializer_class, view,
                                                          request, **kwargs)

            return self.render_form_for_serializer(serializer)
