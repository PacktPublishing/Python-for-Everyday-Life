# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import time

# A context manager that tic-tocs its managed code's execution
class timer(object):

    def __enter__(self):
        self.start = time.time()
        print('Timer starts at: %s' % self.start)
        return self

    def __exit__(self, type, value, traceback):
        self.stop = time.time()
        print('Timer stops at: %s' % self.stop)
        print('Elapsed: %s' % (self.stop - self.start))
        return self