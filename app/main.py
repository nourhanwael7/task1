"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.students import router as students_router

app = FastAPI(title="Students CRUD API", version="1.0.0")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Service health endpoint."""

    return {"status": "ok"}


app.include_router(students_router)
