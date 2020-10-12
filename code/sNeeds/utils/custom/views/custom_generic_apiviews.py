from sNeeds.base.api import generics
from sNeeds.utils.custom.views.custom_mixins import BaseListModelMixin, BaseCreateModelMixin,\
    BaseRetrieveModelMixin, BaseUpdateModelMixin, BaseDestroyModelMixin


class BaseGenericAPIView(generics.CGenericAPIView):

    # the serializer instance that should be used for validating and
    # deserializing requests
    request_serializer_class = None

    request_methods = None

    comment = ""
    description = ""

    def get_request_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing request.
        """
        request_serializer_class = self.get_request_serializer_class()

        if request_serializer_class is None:
            request_serializer_class = self.get_serializer_class()
            kwargs['context'] = self.get_serializer_context()
        else:
            kwargs['context'] = self.get_request_serializer_context()

        return request_serializer_class(*args, **kwargs)

    def get_request_serializer_class(self):
        """
        Return the class to use for the request serializer.
        Defaults to using `self.request_serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        return self.request_serializer_class

    def get_request_serializer_context(self):
        """
        Extra context provided to the request serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    # @classmethod
    # def request_serializer_class_or_regular_serializer_class(cls):
    #     """ Returns the request serializer class if it not None, other wise the normal serializer class"""
    #     request_serializer_class = cls.get_request_serializer_class(cls())
    #     if request_serializer_class is None:
    #         request_serializer_class = cls.get_serializer_class(cls())
    #
    #     return request_serializer_class


    @property
    def request_serializer_class_or_regular_serializer_class(self):
        """ Returns the request serializer class if it not None, other wise the normal serializer class"""
        request_serializer_class = self.get_request_serializer_class()
        if request_serializer_class is None:
            request_serializer_class = self.get_serializer_class()

        return request_serializer_class


class BaseListAPIView(BaseListModelMixin, BaseGenericAPIView):
    """
    Concrete view for listing a queryset.
    """

    def get(self, request, *args, **kwargs):
        """
        List the queryset
        """
        return self.list(request, *args, **kwargs)


class BaseCreateAPIView(BaseCreateModelMixin,
                        BaseGenericAPIView):
    """
    Concrete view for creating a model instance.
    """

    request_methods = ['post']

    def post(self, request, *args, **kwargs):
        """
        Create a new instance
        """
        return self.create(request, *args, **kwargs)


class BaseListCreateAPIView(BaseGenericAPIView,
                            BaseListModelMixin,
                            BaseCreateModelMixin,
                            ):

    request_methods = ['post']

    """
    Concrete view for listing a queryset or creating a model instance.
    """
    def get(self, request, *args, **kwargs):
        """
        List the queryset
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create a new instance
        """
        return self.create(request, *args, **kwargs)


class BaseRetrieveAPIView(BaseRetrieveModelMixin,
                          BaseGenericAPIView):
    """
    Concrete view for retrieving a model instance.
    """

    def get(self, request, *args, **kwargs):
        """Handle get method"""
        return self.retrieve(request, *args, **kwargs)


class BaseDestroyAPIView(BaseDestroyModelMixin,
                         BaseGenericAPIView):
    """
    Concrete view for deleting a model instance.
    """

    def delete(self, request, *args, **kwargs):
        """Handle delete method"""
        return self.destroy(request, *args, **kwargs)


class BaseUpdateAPIView(BaseUpdateModelMixin,
                        BaseGenericAPIView):
    """
    Concrete view for updating a model instance.
    """

    request_methods = ['put', 'patch']


    def put(self, request, *args, **kwargs):
        """Handle put method"""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Handle patch method"""
        return self.partial_update(request, *args, **kwargs)


class BaseRetrieveUpdateAPIView(BaseRetrieveModelMixin,
                                BaseUpdateModelMixin,
                                BaseGenericAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """

    request_methods = ['put', 'patch']

    def get(self, request, *args, **kwargs):
        """Handle get method"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Handle put method"""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Handle patch method"""
        return self.partial_update(request, *args, **kwargs)


class BaseRetrieveDestroyAPIView(BaseRetrieveModelMixin,
                                 BaseDestroyModelMixin,
                                 BaseGenericAPIView):
    """
    Concrete view for retrieving or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        """Handle get method"""
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Handle delete method"""
        return self.destroy(request, *args, **kwargs)


class BaseRetrieveUpdateDestroyAPIView(BaseRetrieveModelMixin,
                                       BaseUpdateModelMixin,
                                       BaseDestroyModelMixin,
                                       BaseGenericAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """

    request_methods = ['put', 'patch']

    def get(self, request, *args, **kwargs):
        """Handle get method"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Handle put method"""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Handle patch method"""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Handle delete method"""
        return self.destroy(request, *args, **kwargs)