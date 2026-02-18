"""Students API router."""

from fastapi import APIRouter, Depends
from pymongo import MongoClient
from pymongo.collection import Collection

from app.database import get_mongo_client, get_students_collection
from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["students"])


def get_collection(client: MongoClient = Depends(get_mongo_client)) -> Collection:
    """Resolve students collection dependency."""

    return get_students_collection(client)


def get_student_service(collection: Collection = Depends(get_collection)) -> StudentService:
    """Resolve student service dependency."""

    repository = StudentRepository(collection)
    return StudentService(repository)


@router.post("", response_model=StudentResponse, status_code=201)
def insert_student(request: StudentCreate, service: StudentService = Depends(get_student_service)) -> StudentResponse:
    """Insert a new student with name and age."""

    return service.insert_student(request)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, service: StudentService = Depends(get_student_service)) -> StudentResponse:
    """Get one student by id."""

    return service.get_student(student_id)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: str,
    request: StudentUpdate,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Update student name and/or age by id."""

    return service.update_student(student_id, request)


@router.delete("/{student_id}")
def delete_student(student_id: str, service: StudentService = Depends(get_student_service)) -> dict[str, str]:
    """Delete one student by id."""

    return service.delete_student(student_id)
