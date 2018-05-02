# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import random

def random_word(length):
    # Get a list of random ints representing ASCII uppercase letters
    # (decimal 65 --> decimal 90)
    random_ints = [random.randint(65, 90) for _ in range(length)]  # COMPREHENSION

    # Turn these ints to strings
    random_strs = [chr(i) for i in random_ints]  # COMPREHENSION

    # Join the strings into a single word
    return ''.join(random_strs)  # STRING JOINING


def random_words_list(n_words, length=7):
    assert n_words is not None  # CHECK FOR NONETHINESS
    assert length is not None   # CHECK FOR NONETHINESS
    assert isinstance(n_words, int)
    assert isinstance(length, int)
    assert n_words > 0
    assert length > 0

    word_list = list()
    for _ in range(n_words):  # USAGE OF IN OPERATOR IN LOOPS
        word_list.append(random_word(length))

    return word_list


def random_words_dict(n_words, length=7):
    words_list = random_words_list(n_words, length)

    # ENUMERATION and COMPREHENSION
    words_dict = {index: word for index, word in enumerate(words_list)}

    return words_dict


if __name__ == '__main__':

    d = random_words_dict(10, length=5)
    non_existing_word = d.get(45, None)  # DICT KEY SAFE ACCESS
    first_word = d.get(0, None)  # DICT KEY SAFE ACCESS

    l = random_words_list(34, length=3)
    first_ten_words = l[:10]  # LIST SLICING
    words_from_ten_to_twenty = l[9:20]  # LIST SLICING
