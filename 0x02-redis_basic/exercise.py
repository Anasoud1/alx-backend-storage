#!/usr/bin/env python3
"""Cache class"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """counts the number of times a method is called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """add and store in redis"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        key = method.__qualname__
        self._redis.rpush(key + ":inputs", str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(key + ":outputs", data)
        return data
    return wrapper


def replay(method: Callable) -> None:
    """display the history of calls of a particular function"""
    r = redis.Redis()
    name = method.__qualname__
    nb_call = r.get(name)
    print(f'{name} was called {nb_call.decode("utf-8")} times:')
    inp = r.lrange(name + ":inputs", 0, -1)
    outp = r.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inp, outp):
        print(f'{name}(*{i.decode("utf-8")}) -> {o.decode("utf-8")}')


class Cache:
    """Define Cache"""
    def __init__(self) -> None:
        """constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key anad return it"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """get data from the cache"""
        data = self._redis.get(key)
        if fn is None:
            return data
        return fn(data)

    def get_str(self, key: str) -> str:
        """get a string from the cache"""
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """get a int from the cache"""
        value = self._redis.get(key)
        return int(value.decode('utf-8'))
