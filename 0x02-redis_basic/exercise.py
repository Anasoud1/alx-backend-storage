#!/usr/bin/env python3
"""Cache class"""
import redis
import uuid
from typing import Union, Optional, Callable


class Cache:
    """Define Cache"""
    def __init__(self) -> None:
        """constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[int, str, bytes, float]) -> str:
        """generate a random key anad return it"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[int, str, bytes,
                                                          float]:
        """get data from the cache"""
        data = self._redis.get(key)
        if (fn is None):
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
