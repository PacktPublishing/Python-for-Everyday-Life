# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# --- USING THE PYTHON STANDARD LIBRARY

# we import two modules of the Python standard library here
import random
import math

def calculate_pi(attempts):
    """
    This function calculates an approximation of Pi using a raw MonteCarlo
    integration technique
    :param: attempts: the number of iterations for the MonteCarlo  method
    :type: attemts: int
    :return: the approximated value of Pi
    """
    assert isinstance(attempts, int), 'you must provide an integer'
    assert attempts > 0, 'you must provide a positive integer'
    falling_inside = 0
    for _ in range(attempts):
        # here we use functionalities provided by random and math modules
        x = random.uniform(0.0, 1.0)
        y = random.uniform(0.0, 1.0)
        if math.sqrt(x**2 + y**2) <= 1:
            falling_inside += 1
    pi = 4 * falling_inside/attempts
    return pi


if __name__ == '__main__':
    iterations = 100000
    result = calculate_pi(iterations)
    print('Approximated value for Pi: {}'.format(result))
    print('Iterations used: {}'.format(iterations))