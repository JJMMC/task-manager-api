import pytest
import os
from app.database import TestSessionLocal, Base, test_engine
import app.models as models
from app.main import app  
from app.database import get_db

Base.metadata.create_all(test_engine)

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    yield
    db_path = "./test_task_manager.db"
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture(autouse=True)
def clean_users_table(get_test_db):
    get_test_db.query(models.User).delete()
    get_test_db.commit()

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


# --- OVERRIDE DE get_db ---
# Permite sustituir la función get_db inyectada en las rutas por Depends
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides = {}
app.dependency_overrides[get_db] = override_get_db