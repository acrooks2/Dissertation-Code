# -*- coding: utf-8 -*-
"""
dump the first level keys from the mongodb
"""
from pymongo import MongoClient
from bson import Code

def get_keys(db, collection):
    client = MongoClient()
    db = client[db]
    map = Code("function() { for (var key in this) { emit(key, null); } }")
    reduce = Code("function(key, stuff) { return null; }")
    result = db[collection].map_reduce(map, reduce, "myresults")
    return result.distinct('_id')

if __name__ == "__main__":
    x = get_keys(name_of_your_database, name_of_your_collection)
    print(x)