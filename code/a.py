# def decorator_func(wrapper_func):
#     def return_func():
#         return wrapper_func()
#     return_func.jafar = "hello"
#     return return_func
#
#
# def hello_func():
#     print("hello")
#
#
# a = decorator_func(hello_func)
# print(a.jafar)

class A:
    a1 = "hello"

    def hello(self):
        return "Hi"

class B(A):
    pass


print(B.__dict__)
print(B.a1)
