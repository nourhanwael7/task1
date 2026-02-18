"""MongoDB connection helpers."""

from typing import Generator

from pymongo import MongoClient
from pymongo.collection import Collection

from app.config import get_settings


def get_mongo_client() -> Generator[MongoClient, None, None]:
    """Yield a MongoDB client and close it after request is done."""

    settings = get_settings()
    client = MongoClient(settings.mongo_uri)
    try:
        yield client
    finally:
        client.close()


def get_students_collection(client: MongoClient) -> Collection:
    """Return the students collection from MongoDB."""

    settings = get_settings()
    return client[settings.database_name][settings.collection_name]
