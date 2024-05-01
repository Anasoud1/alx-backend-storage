#!/usr/bin/env python3
"""Cache class"""
import redis
import uuid
from typing import Union, Any


class Cache:
    """Define Cache"""
    def __init__(self) -> None:
        """constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[int, str, str, float]) -> str:
        """generate a random key anad return it"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
