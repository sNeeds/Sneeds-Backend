from drf_yasg.utils import swagger_auto_schema


def get_class_decorated_view(cls):
    if cls.request_methods is not None:
        # print(cls.__name__)
        decorated_view = swagger_auto_schema(
            request_body=cls().get_request_serializer_class_or_regular_serializer_class(),
            methods=cls.request_methods,
            responses={200: cls().get_serializer_class()},
        )(cls.as_view())
    else:
        # return swagger_auto_schema(
        #     request_body=cls().get_request_serializer_class_or_regular_serializer_class(),
        #     responses={200: cls.serializer_class},
        # )(cls.as_view())
        decorated_view = cls.as_view()
    return decorated_view

