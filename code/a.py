def decorator_func(wrapper_func):
    def return_func():
        return wrapper_func()

    return return_func


def hello_func():
    print("hello")


a = decorator_func(hello_func)
a()