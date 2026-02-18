"""Business logic for student CRUD operations."""

from fastapi import HTTPException, status

from app.models.student import parse_object_id, student_from_mongo
from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate


class StudentService:
    """Service layer that validates and orchestrates student operations."""

    def __init__(self, repository: StudentRepository) -> None:
        self.repository = repository

    def insert_student(self, request: StudentCreate) -> StudentResponse:
        result = self.repository.insert(request.model_dump())
        document = self.repository.find_by_id(result.inserted_id)
        if document is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch created student")
        return student_from_mongo(document)

    def get_student(self, student_id: str) -> StudentResponse:
        oid = self._validated_id(student_id)
        document = self.repository.find_by_id(oid)
        if document is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        return student_from_mongo(document)

    def update_student(self, student_id: str, request: StudentUpdate) -> StudentResponse:
        update_data = request.model_dump(exclude_none=True)
        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one field is required")

        oid = self._validated_id(student_id)
        existing = self.repository.find_by_id(oid)
        if existing is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        self.repository.update(oid, update_data)
        updated = self.repository.find_by_id(oid)
        if updated is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch updated student")
        return student_from_mongo(updated)

    def delete_student(self, student_id: str) -> dict[str, str]:
        oid = self._validated_id(student_id)
        result = self.repository.delete(oid)
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        return {"message": "Student deleted successfully"}

    @staticmethod
    def _validated_id(student_id: str):
        try:
            return parse_object_id(student_id)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
