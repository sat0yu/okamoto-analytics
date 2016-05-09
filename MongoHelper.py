#coding: utf-8;
from __future__ import division, print_function, unicode_literals
from future_builtins import *
import pymongo
import datetime

class MongoHelper:
    def __init__(self, config):
        self.host       = config["host"]
        self.port       = config["port"]
        self.database   = config["database"]
        self.source_collection = config["source_collection"]
        self.result_collection = config["result_collection"]
        self.endpoint   = "mongodb://%s:%s" % (self.host, self.port)
        self.client     = pymongo.MongoClient(self.endpoint)

    def insertResult(self, status):
        collection = self.client[self.database][self.result_collection]
        return collection.insert_one(status.serialize())

    def getLastSegment(self):
        order_by    = [("created_at", pymongo.DESCENDING)]
        collection  = self.client[self.database][self.source_collection]
        cursor      = collection.find().sort(order_by).limit(1)
        return None if cursor.count() == 0  else cursor[0]

    def getLastResult(self):
        order_by = [("created_at", pymongo.DESCENDING)]
        collection = self.client[self.database][self.result_collection]
        cursor      = collection.find().sort(order_by).limit(1)
        return None if cursor.count() == 0  else cursor[0]
