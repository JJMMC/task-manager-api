# Declaramos Modelos/Esquemas de SQLAlchemy
#import database
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


# Definnimos las tablas de nuestra DB para SQLAlchemy
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String,nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    disable = Column(Boolean, default=False)
    
    # Relación con Tareas
    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    done = Column(Boolean, default=False )
    user_id = Column(Integer, ForeignKey('users.id') )

    # Relación inversa con Usuario
    owner = relationship("User", back_populates="tasks")





