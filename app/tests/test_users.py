import pytest
from fastapi import HTTPException
import os
from sqlalchemy.orm import Session
from app.database import TestSessionLocal, Base, test_engine
from app.services import users_service
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


## CREATING USERS ##

# Create a user.
def test_create_users(get_test_db: Session):
    # Crea un usuario de prueba con todos los campos requeridos
    new_user = create_test_user(get_test_db)
    assert isinstance(new_user, models.User)
    assert new_user.email == "testuser@example.com" # type: ignore

# What happends if the email all ready exists.
def test_email_already_exists(get_test_db: Session):
    # Crea un usuario de prueba con todos los campos requeridos
    create_test_user(get_test_db)
    
    with pytest.raises(HTTPException) as exc_info:
        create_test_user(get_test_db)
        
    assert exc_info.value.status_code == 400


## GETTING USERS ##

def test_get_all_users(get_test_db: Session):
    # Crea dos usuarios de prueba
    create_test_user(get_test_db, name="Test1", user_name="testuser1", email="testuser1@example.com")
    create_test_user(get_test_db, name="Test2", user_name="testuser2", email="testuser2@example.com")
    

    # Obtiene todos los usuarios y verifica que hay 2
    all_users = users_service.get_users(get_test_db)
    assert len(all_users) == 2
    
    # Opcional: verifica que los emails están en la lista
    emails = [user.email for user in all_users]
    assert "testuser1@example.com" in emails
    assert "testuser2@example.com" in emails

def test_get_users_by_id(get_test_db: Session):
    # Crea usuario de prueba y guarda el objeto retornado
    new_user = create_test_user(get_test_db)
    new_user_id = new_user.id  # Usa el ID real asignado por la base de datos
    test_user = users_service.get_user_by_id(get_test_db, new_user_id) # type: ignore
    assert new_user_id == test_user.id # type: ignore
    assert test_user.email == "testuser@example.com"# type: ignore

def test_not_users_by_id(get_test_db: Session):
    # Crea usuario de prueba y lo almacena en DB
    create_test_user(get_test_db)
    new_user_id = 998
    with pytest.raises(HTTPException) as exc_info:
        users_service.get_user_by_id(get_test_db, new_user_id)
        
    assert exc_info.value.status_code == 404


## UPDATING USER ##

def test_put_user(get_test_db: Session):
    # Crea usuario de prueba y guarda el objeto retornado
    new_user = create_test_user(get_test_db)
    user_id = new_user.id
    
    # Datos con los que queremos actualizar
    data_to_update = schemas.UserCreate(
        name='name_mod',
        surname='surname_mod',
        user_name='user_name_mod',
        email='email_mod@example.com',
        password='password_mod'
    )

    # Actualizamos los datos del usuario
    users_service.put_user(data_to_update, get_test_db, user_id) # type: ignore
    user_updated = users_service.get_user_by_id(get_test_db, user_id) # type: ignore

    assert user_updated.name == 'name_mod' # type: ignore

def test_put_no_user(get_test_db: Session):
    # Creamos un usuario y almacenamos en la DB
    create_test_user(get_test_db)
    
    # Usa un id que no existe (por ejemplo, 999)
    user_id = 998
    data_to_update = schemas.UserCreate(
        name='name_mod',
        surname='surname_mod',
        user_name='user_name_mod',
        email='email_mod@example.com',
        password='password_mod'
    )
    with pytest.raises(HTTPException) as exc_info:
        users_service.put_user(data_to_update, get_test_db, user_id)
    assert exc_info.value.status_code == 404


## DELETING USER ##

def test_delete_user(get_test_db: Session):
    # Crea usuario de prueba y guarda el objeto retornado
    new_user = create_test_user(get_test_db)
    user_id = new_user.id
    #user_id = 1
    

    users_service.delete_user(user_id, get_test_db) # type: ignore
    assert len(users_service.get_users(get_test_db)) == 0

def test_delete_no_user(get_test_db: Session):
    user_id = 998
    with pytest.raises(HTTPException) as exc_info:
        users_service.delete_user(user_id, get_test_db)
    assert exc_info.value.status_code == 404