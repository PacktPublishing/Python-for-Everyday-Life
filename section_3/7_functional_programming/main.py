# -*- coding: utf-8 -*-
# !/usr/bin/env python3

if __name__ == '__main__':

    countries = ['IT', 'ES', 'DE', 'FR', 'US', 'UK', 'JP', 'BR']


    # -- MAP --
    turn_to_lowercase = lambda c: c.lower()
    lowercased_countries = map(turn_to_lowercase, countries)

    print('\nLower cased countries:')
    for country in lowercased_countries:
        print(country)


    # -- FILTER --
    begins_by_vowel = lambda c: c[0].lower() in 'aeiou'
    vowel_countries = filter(begins_by_vowel, countries)

    print('\nCountries beginning with vowel:')
    for country in vowel_countries:
        print(country)


    # -- REDUCE --
    from functools import reduce
    print('\nSumming the first ten integers:')
    result = reduce(lambda a, b: a+b, range(1, 11))
    print(result)


    # -- RECURSION --
    def factorial(n):
        return 1 if n == 0 else n * factorial(n-1)
    number = 20
    print('\nFactorial of {}: {}'.format(number, factorial(number)))


