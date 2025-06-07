import pytest
import os
from sqlalchemy.orm import Session
from app.database import TestSessionLocal, Base, test_engine
from app.services import users_service
import app.schemas as schemas
import app.models as models


Base.metadata.create_all(test_engine)


## FIXTURES ##

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    yield
    # Elimina el archivo de la base de datos de pruebas al final de la sesión
    db_path = "./test_task_manager.db"
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


## TESTS ##

def test_create_users(get_test_db: Session):
    # Crea un usuario de prueba con todos los campos requeridos
    new_user_data = schemas.UserCreate(
        name="Test",
        surname="User",
        user_name="testuser",
        email="testuser@example.com",
        password="testpassword"
    )
    new_user = users_service.create_user(get_test_db, new_user_data)
    assert isinstance(new_user, models.User)
    assert new_user.email == "testuser@example.com" # type: ignore


def test_if_email_exists(get_test_db: Session):
    pass

