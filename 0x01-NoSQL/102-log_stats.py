#!/usr/bin/env python3
"""Script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx_coll = client.logs.nginx

    print(f"{nginx_coll.count_documents({})} logs")

    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    print("Methods:")
    for method in methods:
        query = nginx_coll.count_documents({'method': method})
        print(f"\tmethod {method}: {query}")

    status = nginx_coll.count_documents({"method": "GET", "path": "/status"})
    print(f'{status} status check')

    print("IPs:")
    ips = []
    for col in nginx_coll.find():
        if col.get('ip') not in ips:
            ips.append(col.get('ip'))

    list_ips = nginx_coll.aggregate([
                {'$group': {
                    '_id': '$ip',
                    'total_req': {'$sum': 1}}},
                {'$sort': {'total_req': -1}},
                {'$limit': 10}
          ])
    for ip in list_ips:
        print(f'\t{ip.get("_id")}: {ip.get("total_req")}')
