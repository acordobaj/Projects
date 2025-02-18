from pymongo import MongoClient


class DBManager:
    def __init__(self, db_name="project_management"):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]
