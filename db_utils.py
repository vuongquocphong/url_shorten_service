from pymongo import MongoClient
import sys

class DB:
    def __init__(self):
        try:
            print("Connecting to database")
            self.client = MongoClient("mongodb://localhost:27017/")
            self.client.admin.command('ping')
            print("Connected to database")
            self.db = self.client["shortened_url_db"]
            self.collection = self.db["urls"]
        except Exception as e:
            print("Error connecting to database")
            sys.exit(1)
    def insert(self, data):
        self.collection.insert_one(data)
    def find(self, query):
        return self.collection.find_one(query)
    def delete(self, query):
        self.collection.delete_one(query)
    def update(self, query, data):
        self.collection.update_one(query, {"$set": data})