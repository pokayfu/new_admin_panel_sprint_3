import logging
from functools import wraps
from time import sleep


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            t = 0
            iteration = 1
            while True:
                if t < border_sleep_time:
                    t = start_sleep_time * pow(factor, iteration)
                else:
                    t = border_sleep_time
                iteration += 1
                try:
                    sleep(t)
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(e)
                    continue
        return inner
    return func_wrapper
