#!/usr/bin/env python3
"""top_students modules"""


def top_students(mongo_collection):
    """function that returns all students sorted by average score"""
    students = mongo_collection.aggregate([
        {"$project": {
            '_id': 1,
            'name': 1,
            'averageScore': {'$avg': '$topics.score'}
            }},
        {"$sort": {'averageScore': -1}}
    ])

    unique_st = []
    names_seen = []
    for item in students:
        name = item['name']
        if name not in names_seen:
            unique_st.append(item)
            names_seen.append(name)
    return unique_st
