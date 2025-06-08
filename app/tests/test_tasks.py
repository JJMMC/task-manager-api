import pytest
from fastapi import HTTPException
import os
from sqlalchemy.orm import Session
from app.database import TestSessionLocal, Base, test_engine
from app.services import users_service, tasks_service
import app.schemas as schemas
import app.models as models


Base.metadata.create_all(test_engine)


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

def test_create_task(get_test_db):
    # 1. Crea un usuario de prueba
    user = create_test_user(get_test_db)

    # 2. Creamos la tarea con la funcion helper
    task = create_test_task(get_test_db, user)

    # 4. Comprueba que la tarea se ha creado correctamente
    assert task.title == "Test Task" # type: ignore
    assert task.description == "Test Description" # type: ignore
    assert task.user_id == user.id # type: ignore

def test_create_task_with_none_description(get_test_db):
    user = create_test_user(get_test_db)
    with pytest.raises(Exception):
        create_test_task(get_test_db, user, title="title", description=None)  # type: ignore

def test_update_task_partial_data(get_test_db):
    user = create_test_user(get_test_db)
    task = create_test_task(get_test_db, user)
    # Solo actualiza el título
    updated_data = schemas.TaskCreate(title="Nuevo título", description=task.description)
    updated_task = tasks_service.put_task(updated_data, task.id, get_test_db, user)
    assert updated_task.title == "Nuevo título"
    assert updated_task.description == task.description

def test_toggle_task_done(get_test_db):
    user = create_test_user(get_test_db)
    task = create_test_task(get_test_db, user)
    # Marcar como hecha
    updated_data = schemas.TaskCreate(title=task.title, description=task.description, done=True)
    updated_task = tasks_service.put_task(updated_data, task.id, get_test_db, user)
    assert updated_task.done is True
    # Desmarcar
    updated_data = schemas.TaskCreate(title=task.title, description=task.description, done=False)
    updated_task = tasks_service.put_task(updated_data, task.id, get_test_db, user)
    assert updated_task.done is False

def test_list_tasks_when_none(get_test_db):
    user = create_test_user(get_test_db, user_name="emptyuser", email="empty@example.com")
    tasks = tasks_service.get_user_tasks(get_test_db, user)
    assert tasks == []

def test_update_other_users_task(get_test_db):
    user1 = create_test_user(get_test_db, user_name="user1", email="user1@example.com")
    user2 = create_test_user(get_test_db, user_name="user2", email="user2@example.com")
    task = create_test_task(get_test_db, user1)
    updated_data = schemas.TaskCreate(title="Hack", description="Hack", done=True)
    with pytest.raises(HTTPException):
        tasks_service.put_task(updated_data, task.id, get_test_db, user2)

def test_delete_other_users_task(get_test_db):
    user1 = create_test_user(get_test_db, user_name="user1", email="user1@example.com")
    user2 = create_test_user(get_test_db, user_name="user2", email="user2@example.com")
    task = create_test_task(get_test_db, user1)
    with pytest.raises(HTTPException):
        tasks_service.delete_task(task.id, get_test_db, user2)

def test_task_created_at_timestamp(get_test_db):
    user = create_test_user(get_test_db)
    task = create_test_task(get_test_db, user)
    assert hasattr(task, "created_at")
    assert task.created_at is not None

def test_get_task_by_nonexistent_id(get_test_db):
    user = create_test_user(get_test_db)
    with pytest.raises(HTTPException) as exc_info:
        tasks_service.get_user_task_by_id(123456, get_test_db, user)
    assert exc_info.value.status_code == 404

def test_delete_all_tasks_and_check_empty(get_test_db):
    user = create_test_user(get_test_db)
    t1 = create_test_task(get_test_db, user, title="T1")
    t2 = create_test_task(get_test_db, user, title="T2")
    tasks_service.delete_task(t1.id, get_test_db, user)
    tasks_service.delete_task(t2.id, get_test_db, user)

    tasks = tasks_service.get_user_tasks(get_test_db, user)
    assert tasks == []






