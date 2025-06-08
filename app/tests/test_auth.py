import pytest
from fastapi import HTTPException
from app.services import users_service, tasks_service
import app.schemas as schemas
from fastapi.testclient import TestClient
from app.main import app


# Creamos el objeto client que nos permite simular el server activo
client = TestClient(app)

##################
## HELPER FUNCT ##
##################

def create_test_user(db, name="Test", surname="User", user_name="testuser", email="testuser@example.com", password="testpassword"):
    user_data = schemas.UserCreate(
        name=name,
        surname=surname,
        user_name=user_name,
        email=email,
        password=password
    )
    return users_service.create_user(db, user_data)

def create_test_task(db, current_user, title="Test Task", description="Test Description"):
    task_data = schemas.TaskCreate(
        title=title,
        description=description
    )

    return tasks_service.create_task(task_data, db, current_user)


###########
## TESTS ##
###########

def test_login_ok(get_test_db):
    # Crear usuario de prueba en la base de datos
    create_test_user(get_test_db, user_name="testuser", email="testuser@example.com", password="testpassword")
    # Simular petición de login
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(get_test_db):
    create_test_user(get_test_db, user_name="testuser2", email="testuser2@example.com", password="correctpassword")
    response = client.post(
        "/token",
        data={"username": "testuser2", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_login_nonexistent_user(get_test_db):
    response = client.post(
        "/token",
        data={"username": "nouser", "password": "nopassword"}
    )
    assert response.status_code == 401

def test_protected_endpoint_no_token():
    response = client.get("/tasks")  # Cambia por un endpoint protegido real
    assert response.status_code == 401

def test_protected_endpoint_invalid_token():
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/tasks", headers=headers)  # Cambia por un endpoint protegido real
    assert response.status_code == 401