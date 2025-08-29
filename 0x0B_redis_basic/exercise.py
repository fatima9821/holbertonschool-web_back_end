#!/usr/bin/env python3
"""Redis basic"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Decorator that counts call function"""
    @wraps(method)
    def wrapper(self, *args, **kwds):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of the function"""
    @wraps(method)
    def wrapper(self, *args, **kwds):
        key = method.__qualname__
        input_key = key + ":inputs"
        output_key = key + ":outputs"
        data = str(args)
        self._redis.rpush(input_key, data)
        output = method(self, *args, **kwds)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(fn: Callable):
    """Function that display the history of calls function"""
    redis_instance = redis.Redis()
    function_name = fn.__qualname__
    call_count = redis_instance.get(function_name)
    try:
        call_count = call_count.decode('utf-8')
    except Exception:
        call_count = 0
    time_str = "time:" if call_count == 1 else "times:"
    print(f'{function_name} was called {call_count} {time_str}')
    inputs = redis_instance.lrange(function_name + ":inputs", 0, -1)
    outputs = redis_instance.lrange(function_name + ":outputs", 0, -1)
    for input_value, output_value in zip(inputs, outputs):
        try:
            input_value = input_value.decode('utf-8')
        except Exception:
            input_value = ""
        try:
            output_value = output_value.decode('utf-8')
        except Exception:
            output_value = ""
        print(f'{function_name}(*{input_value}) -> {output_value}')


class Cache():
    """Cache class to store data using Redis. """

    def __init__(self):
        """Initialize a Redis instance and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return the generated key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Retrieve data from Redis and apply the conversion if provided."""
        value = self._redis.get(key)
        return value if not fn else fn(value)

    def get_int(self, key: str) -> int:
        """Retrieve an integer from Redis."""
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value

    def get_str(self, key):
        """ Retrieve a string from redis """
        value = self._redis.get(key)
        return value.decode("utf-8")
