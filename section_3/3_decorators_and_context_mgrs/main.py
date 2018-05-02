# -*- coding: utf-8 -*-
# !/usr/bin/env python3

if __name__ == '__main__':
    from ctx_mgr import timer
    from decos import greet


    # --- CONTEXT MANAGERS AND DECORATORS ---

    # Our code to be profiled
    def kill_time():
        for _ in range(9999999):
            pass

    print('Running with context manager')
    with timer():
        kill_time()


    # ... but code should always greet
    @greet
    def greeting_kill_time():
        kill_time()

    print('Running with context manager and decorator')
    with timer():
        greeting_kill_time()

