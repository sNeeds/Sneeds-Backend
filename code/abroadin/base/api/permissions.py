def permission_class_factory(cls: object, apply_on: list):
    _ALL_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]

    def decorator(original_func, method_in: list):
        def wrapper(self, request, *args, **kwargs):
            print("\nrequest.method", request.method)
            print("method_in", method_in)

            if request.method in method_in:
                return original_func(self, request, *args, **kwargs)

            return True

        return wrapper

    allowed_methods = [e.upper() for e in apply_on]
    if not set(allowed_methods) <= set(_ALL_METHODS):
        raise ValueError(f"Apply on methods are {apply_on}, Allowed methods must be sublist of: {_ALL_METHODS}")

    cls.has_permission = decorator(cls.has_permission, allowed_methods)
    return cls
