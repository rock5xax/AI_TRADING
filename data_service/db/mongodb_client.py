from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, uri, database_name):
        self.client = MongoClient(uri)
        self.db = self.client[database_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]
