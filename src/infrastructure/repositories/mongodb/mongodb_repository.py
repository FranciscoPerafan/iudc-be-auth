from pymongo import MongoClient
from bson import ObjectId

class MongodbRepository:
    def __init__(self, string_connection, name_db, collection_name):
        self.client = MongoClient(string_connection)
        self.db = self.client[name_db]
        self.collection = self.db[collection_name]

    def get(self, details=[], **kwargs):
        pipeline = [
            {"$match": kwargs},
        ]
        pipeline = self.add_pipeline(pipeline, details)

        result = list(self.collection.aggregate(pipeline))
        return result[0] if result else None

    def get_all(self, page: int, page_size: int, details=[], **kwargs):
        skip = (page - 1) * page_size

        query = {}
        for key, value in kwargs.items():
            if value:
                if isinstance(value, str):
                    query[key] = {"$regex": value, "$options": "i"}
                else:
                    query[key] = value

        total_documents = self.collection.count_documents(query)
        if total_documents == 0:
            return [], 0
        if total_documents <= skip:
            raise ValueError("Page not found")
        
        pipeline = [
            {"$match": query},
            {"$skip": skip},
            {"$limit": page_size},
        ]
        pipeline = self.add_pipeline(pipeline, details)
        data = list(self.collection.aggregate(pipeline))
        total_pages = (total_documents + page_size - 1) // page_size
        return data, total_pages

    def create(self, **kwargs):
        return self.collection.insert_one(kwargs)

    def update(self, id: ObjectId, update_data: dict, array_filters=None):
        return self.collection.update_one(
            {"_id": id},
            update_data,
            array_filters=array_filters or []
        )

    def add_pipeline(self, pipeline, details):
        return pipeline + details