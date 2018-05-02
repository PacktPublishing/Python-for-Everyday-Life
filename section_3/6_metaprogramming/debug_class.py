# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Function decorator: prints when a function is called along
# with its parameters
def debug(func):
    def decorated(*args, **kwargs):
        print('Function: {} called with args: {} and kwargs: {}'.format(
            func.__name__,
            args,
            kwargs))
        return func(*args, **kwargs)
    return decorated


# Class decorator: decorate all class methods with the
# @debug decorator
def debug_all_functions(cls_obj):
    for name, val in vars(cls_obj).items():
        if callable(val):
            setattr(cls_obj, name, debug(val))
    return cls_obj


# Metaclass: generate a class having all methods debuggable
class DebugMetaclass(type):
    def __new__(mcs, cls_name, bases, cls_dict):
        cls_obj = super().__new__(mcs, cls_name, bases, cls_dict)
        cls_obj = debug_all_functions(cls_obj)
        return cls_obj


# Finally, our class
class MyClass(metaclass=DebugMetaclass):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def foo(self):
        return self.a

    def bar(self):
        return self.b


if __name__ == '__main__':
    instance = MyClass('hello', 'world')
    instance.foo()
    instance.bar()