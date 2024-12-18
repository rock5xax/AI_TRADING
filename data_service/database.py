from pymongo import MongoClient

class MongoDB:
    def __init__(self, db_config):
        self.client = MongoClient(db_config["uri"])
        self.database = self.client[db_config["database"]]

    def store_data(self, collection_name, data):
        collection = self.database[collection_name]
        if isinstance(data, list):  # Store multiple documents
            collection.insert_many(data)
        else:  # Store a single document
            collection.insert_one(data)

    def fetch_data(self, collection_name, query=None):
        collection = self.database[collection_name]
        return list(collection.find(query or {}))
