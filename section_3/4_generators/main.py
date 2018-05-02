# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# Generator function for a finite generator of Fibonacci numbers
def generate_fibonacci_under(max):
    a, b = 0, 1
    while a < max:
        yield a
        a, b = b, a + b


# Generator function for an infinite generator of Fibonacci numbers
def generate_fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


if __name__ == '__main__':

    # finite loop using generator expressions
    generator = (n for n in [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89])
    for f in generator:
        print(f)

    # finite loop using generator functions
    generator = generate_fibonacci_under(100)
    for f in generator:
        print(f)

    # infinite loop with generator functions
    generator = generate_fibonacci()
    while True:
        print(next(generator))