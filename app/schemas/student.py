"""Pydantic schemas for student payloads."""

from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    """Payload used to insert a student."""

    name: str = Field(..., min_length=1, max_length=120)
    age: int = Field(..., ge=1, le=120)


class StudentUpdate(BaseModel):
    """Payload used to update a student."""

    name: str | None = Field(default=None, min_length=1, max_length=120)
    age: int | None = Field(default=None, ge=1, le=120)


class StudentResponse(BaseModel):
    """Response object for student data."""

    id: str
    name: str
    age: int
