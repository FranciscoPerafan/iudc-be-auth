import os

from src.infrastructure.repositories.mongodb.mongodb_repository import MongodbRepository

COLLECTION_NAME="users"


class UserRepository(MongodbRepository):
    def __init__(self):
        user = os.getenv("MONGO_DATABASE_USERNAME")
        password = os.getenv("MONGO_DATABASE_PASSWORD")
        cluster = os.getenv("MONGO_DATABASE_CLUSTER")
        string_connection = f"mongodb+srv://{user}:{password}@{cluster}/"
        super().__init__(
            string_connection,
            os.getenv("MONGO_DATABASE_NAME"),
            COLLECTION_NAME,
        )
