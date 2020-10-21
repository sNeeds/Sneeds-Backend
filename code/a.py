class T:
    def foo(cls):
        print("OOPPPPP")

    pass


def foo(cls):
    print(cls)
    return cls.__mro__


T.foo = foo
print(T.foo(T))
