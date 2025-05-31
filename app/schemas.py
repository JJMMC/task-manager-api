from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ----------------
# SCHEMAS PYDANTIC - TASKS 
# ----------------
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


# ----------------
# SCHEMAS PYDANTIC - USERS
# ----------------

class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    disable: bool | None = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True # Para convertir entre SQLAlchemy y Pydantic
  
