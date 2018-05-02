# -*- coding: utf-8 -*-
# !/usr/bin/env python3

def greet(func):
    def decorated_func(*args, **kwargs):
        print('Hello!')
        return func(*args, **kwargs)
    return decorated_func