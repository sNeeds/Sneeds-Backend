from rest_framework import mixins, status
from rest_framework.response import Response


class BaseCreateModelMixin(mixins.CreateModelMixin):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        """
        Create a model instance.
        """
        request_serializer = self.get_request_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        self.perform_create(request_serializer)
        response_serializer = self.get_serializer(
            instance=request_serializer.instance
        )
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED, headers=headers
        )


class BaseListModelMixin(mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        return super(BaseListModelMixin, self).list(request, *args, **kwargs)


class BaseRetrieveModelMixin(mixins.RetrieveModelMixin):
    pass


class BaseUpdateModelMixin(mixins.UpdateModelMixin):
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request_serializer = self.get_request_serializer(
            instance, data=request.data, partial=partial
        )
        request_serializer.is_valid(raise_exception=True)
        self.perform_update(request_serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response_serializer = self.get_serializer(
            instance=request_serializer.instance
        )

        return Response(response_serializer.data)


class BaseDestroyModelMixin(mixins.DestroyModelMixin):
    pass
