# Test cases for the Flask application

import pytest

from app.main import create_app


@pytest.fixture
def client():
    app = create_app()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["application"] == "Python Task Manager"


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200

    assert response.get_json() == {
        "status": "healthy"
    }


def test_get_tasks(client):
    response = client.get("/tasks")

    assert response.status_code == 200

    tasks = response.get_json()

    assert isinstance(tasks, list)

    assert len(tasks) >= 2


def test_get_existing_task(client):
    response = client.get("/tasks/1")

    assert response.status_code == 200

    task = response.get_json()

    assert task["id"] == 1
    assert task["title"] == "Learn Docker"


def test_get_nonexistent_task(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404

    assert response.get_json()["error"] == "Task not found"


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Learn GitHub Actions"
        }
    )

    assert response.status_code == 201

    task = response.get_json()

    assert task["title"] == "Learn GitHub Actions"
    assert task["completed"] is False


def test_create_task_without_title(client):
    response = client.post(
        "/tasks",
        json={}
    )

    assert response.status_code == 400

    assert response.get_json()["error"] == "Task title is required"


def test_update_task(client):
    response = client.put(
        "/tasks/1",
        json={
            "title": "Learn Docker Advanced",
            "completed": True
        }
    )

    assert response.status_code == 200

    task = response.get_json()

    assert task["title"] == "Learn Docker Advanced"
    assert task["completed"] is True


def test_update_nonexistent_task(client):
    response = client.put(
        "/tasks/999",
        json={
            "title": "Updated task"
        }
    )

    assert response.status_code == 404


def test_delete_task(client):
    response = client.delete("/tasks/1")

    assert response.status_code == 200

    assert response.get_json()["message"] == "Task deleted successfully"


def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
