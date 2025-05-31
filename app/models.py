# Declaramos Modelos/Esquemas de SQLAlchemy
#import database
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from datetime import datetime
from app.database import Base


# Definnimos las tablas de nuestra DB para SQLAlchemy
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    done = Column(Boolean, default=False )



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    disable = Column(Boolean, default=False)
    





