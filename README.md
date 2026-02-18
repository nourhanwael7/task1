# Students CRUD API (FastAPI + MongoDB)

A clean, organized FastAPI project with **4 endpoints** for students:

1. Insert student
2. Get student
3. Update student
4. Delete student

> No Docker required.

## Stack

- FastAPI
- MongoDB (local installation)
- PyMongo
- Pytest

## Project Structure

```text
app/
  api/students.py            # Endpoints
  config.py                  # Environment settings
  database.py                # Mongo connection helpers
  main.py                    # FastAPI app
  models/student.py          # Mongo <-> API transformations
  repositories/student_repository.py
  schemas/student.py         # Request/response models
  services/student_service.py
tests/
  test_students_api.py
```

## Prerequisites

- Python 3.11+
- MongoDB running locally on `mongodb://localhost:27017`

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs:
- Swagger UI: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`

## Environment Variables

Create `.env` file (optional):

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=school
MONGO_COLLECTION_NAME=students
```

## Endpoints

### 1) Insert
`POST /students`

Body:

```json
{
  "name": "Sara",
  "age": 20
}
```

### 2) Get
`GET /students/{student_id}`

### 3) Update
`PUT /students/{student_id}`

Body (one or both fields):

```json
{
  "name": "Sarah",
  "age": 21
}
```

### 4) Delete
`DELETE /students/{student_id}`

## Run Tests

```bash
pytest -q
```
