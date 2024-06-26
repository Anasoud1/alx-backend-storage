#!/usr/bin/env python3
"""schools_by_topic module"""


def schools_by_topic(mongo_collection, topic):
    """function that returns the list of school having a specific topic"""
    doc = mongo_collection.find({"topics": topic})
    return list(doc)
