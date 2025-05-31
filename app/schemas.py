from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Modelos de pydantic de Validación de datos que vamos a utilizar:

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True # Para convertir entre SQLAlchemy y Pydantic


# class UserBase(BaseModel):
#     id: int
#     name: str
#     surname: str
#     email: EmailStr
#     password: str
#     disable: bool | None = None

