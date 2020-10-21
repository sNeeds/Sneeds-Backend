def permission_class_factory(cls: object, allowed_methods: list):
    _ALL_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]

    def decorator(original_func, method_in: list):
        def _wrapper(self, request, *args, **kwargs):
            if request.method in method_in:
                return original_func(self, request, *args, **kwargs)

            self.message = "{req_method} is not allowed. Available methods are: {method_in}".format(
                req_method=request.method,
                method_in=method_in
            )
            return False

        return _wrapper

    allowed_methods = [e.upper() for e in allowed_methods]
    if not set(allowed_methods) <= set(_ALL_METHODS):
        raise ValueError(f"Allowed methods are {allowed_methods}, Allowed methods must be sublist of: {_ALL_METHODS}")
    cls.has_permission = decorator(cls.has_permission, allowed_methods)
    return cls
