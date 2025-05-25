# Declaramos Modelos/Esquemas de SQLAlchemy
import database
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from datetime import datetime
from database import Base


#La clase Producto del código representa la tabla de nuestra DB
class User(database.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String)
    disable = Column(Boolean, default=False)
    

    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

    def __repr__(self):
        return f'User ({self.nombre}, {self.email})'

    def __str__(self):
        return str(getattr(self, "nombre", ""))
    



class Task(database.Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    done = Column(Boolean, default=False )