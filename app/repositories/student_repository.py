"""Data access layer for students collection."""

from typing import Any

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult


class StudentRepository:
    """Repository to manage persistence operations for students."""

    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def insert(self, payload: dict[str, Any]) -> InsertOneResult:
        return self.collection.insert_one(payload)

    def find_by_id(self, student_id: ObjectId) -> dict[str, Any] | None:
        return self.collection.find_one({"_id": student_id})

    def update(self, student_id: ObjectId, payload: dict[str, Any]) -> UpdateResult:
        return self.collection.update_one({"_id": student_id}, {"$set": payload})

    def delete(self, student_id: ObjectId) -> DeleteResult:
        return self.collection.delete_one({"_id": student_id})
