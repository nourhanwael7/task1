"""Domain model transformations for student documents."""

from typing import Any

from bson import ObjectId

from app.schemas.student import StudentResponse


def student_from_mongo(document: dict[str, Any]) -> StudentResponse:
    """Convert raw MongoDB document to API response model."""

    return StudentResponse(
        id=str(document["_id"]),
        name=document["name"],
        age=document["age"],
    )


def parse_object_id(student_id: str) -> ObjectId:
    """Parse and validate student id as MongoDB ObjectId."""

    if not ObjectId.is_valid(student_id):
        raise ValueError("Invalid student id format")
    return ObjectId(student_id)
