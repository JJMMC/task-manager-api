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



##############
## FIXTURES ##
##############

# Fixture para eliminar la base de datos de pruebas al final de la sesión de tests
@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    yield
    db_path = "./test_task_manager.db"
    if os.path.exists(db_path):
        os.remove(db_path)

# Fixture para eliminar datos en tabla de usuario al final de cada tests
@pytest.fixture(autouse=True)
def clean_users_table(get_test_db):
    get_test_db.query(models.User).delete()
    get_test_db.commit()

# Fixture para eliminar datos en tabla de usuario al final de cada tests
@pytest.fixture(autouse=True)
def clean_task_table(get_test_db):
    get_test_db.query(models.Task).delete()
    get_test_db.commit()

@pytest.fixture
def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()



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

