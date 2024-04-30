#!/usr/bin/env python3
"""Script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


client = MongoClient("mongodb://127.0.0.1:27017")
nginx_coll = client.logs.nginx

print(f"{nginx_coll.count_documents({})} logs")

methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
print("Methods:")
for method in methods:
    query = nginx_coll.count_documents({'method': method})
    print(f"\tmethod {method}: {query}")


print(f'{nginx_coll.count_documents({"path": "/status"})} status check')
