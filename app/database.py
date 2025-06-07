# CONEXION CON LA BASE DE DATOS
from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()

### TEST ###
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_task_manager.db"

test_engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


### MAIN ###
SQLALCHEMY_DATABASE_URL = "sqlite:///./task_manager.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
