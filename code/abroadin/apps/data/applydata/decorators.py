from functools import wraps


def regular_certificate_or_none(function):
    @wraps(function)
    def wrap(self, *args, **kwargs):
        if self.is_regular_language_certificate_instance():
            return function(self, *args, **kwargs)
        return None

    return wrap


def set_variable(func, var_name, var):
    def function_wrapper(self):
        result = func(self)
        setattr(func, var_name, var)
        return result
    return function_wrapper

