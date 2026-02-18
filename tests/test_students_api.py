"""API tests for student CRUD endpoints."""

from collections.abc import Generator

from bson import ObjectId
from fastapi.testclient import TestClient

from app.api.students import get_collection
from app.main import app


class FakeCollection:
    """Small in-memory collection compatible with repository operations."""

    def __init__(self) -> None:
        self.storage: dict[ObjectId, dict] = {}

    def insert_one(self, payload: dict):
        inserted_id = ObjectId()
        self.storage[inserted_id] = {"_id": inserted_id, **payload}

        class Result:
            pass

        result = Result()
        result.inserted_id = inserted_id
        return result

    def find_one(self, query: dict):
        return self.storage.get(query["_id"])

    def update_one(self, query: dict, payload: dict):
        oid = query["_id"]
        if oid in self.storage:
            self.storage[oid].update(payload["$set"])

        class Result:
            pass

        result = Result()
        result.matched_count = 1 if oid in self.storage else 0
        return result

    def delete_one(self, query: dict):
        oid = query["_id"]
        existed = oid in self.storage
        if existed:
            del self.storage[oid]

        class Result:
            pass

        result = Result()
        result.deleted_count = 1 if existed else 0
        return result


def collection_override_factory(collection: FakeCollection):
    def _override() -> Generator[FakeCollection, None, None]:
        yield collection

    return _override


def test_students_crud_flow() -> None:
    collection = FakeCollection()
    app.dependency_overrides[get_collection] = collection_override_factory(collection)
    client = TestClient(app)

    create_response = client.post("/students", json={"name": "Mona", "age": 23})
    assert create_response.status_code == 201
    created = create_response.json()

    student_id = created["id"]

    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Mona"

    update_response = client.put(f"/students/{student_id}", json={"age": 24})
    assert update_response.status_code == 200
    assert update_response.json()["age"] == 24

    delete_response = client.delete(f"/students/{student_id}")
    assert delete_response.status_code == 200

    missing_response = client.get(f"/students/{student_id}")
    assert missing_response.status_code == 404

    app.dependency_overrides.clear()


def test_invalid_id_returns_400() -> None:
    collection = FakeCollection()
    app.dependency_overrides[get_collection] = collection_override_factory(collection)
    client = TestClient(app)

    response = client.get("/students/not-valid-object-id")

    assert response.status_code == 400
    app.dependency_overrides.clear()
