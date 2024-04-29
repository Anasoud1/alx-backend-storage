#!/usr/bin/env python3
"""insert_school module"""


def insert_school(mongo_collection, **kwargs):
    """function that inserts a new document in a collection"""
    return mongo_collection.insert(kwargs)
