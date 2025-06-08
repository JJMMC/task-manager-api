from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from pydantic import ConfigDict


# ----------------
# SCHEMAS PYDANTIC - USERS
# ----------------

class UserBase(BaseModel):
    name: str
    surname: str
    user_name: str
    email: EmailStr
    #hashed_password: str
    disable: bool | None = None

class TaskInUser(BaseModel):
    id: int
    title: str
    done: bool

    model_config = ConfigDict(from_attributes=True) # Para convertir entre SQLAlchemy y Pydantic
    # class Config:
    #     from_attributes = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    tasks: List[TaskInUser] = []  # Relación uno a muchos
    

    model_config = ConfigDict(from_attributes=True) # Para convertir entre SQLAlchemy y Pydantic
    # class Config:
    #     from_attributes = True # Para convertir entre SQLAlchemy y Pydantic


# ----------------
# SCHEMAS PYDANTIC - TASKS 
# ----------------

class TaskBase(BaseModel):
    title: str
    description: str
    done: bool = False

class UserInTask(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True) # Para convertir entre SQLAlchemy y Pydantic
    # class Config:
    #     from_attributes = True

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime
    owner: Optional[UserInTask]
    

    model_config = ConfigDict(from_attributes=True) # Para convertir entre SQLAlchemy y Pydantic
    # class Config:
    #     from_attributes = True # Para convertir entre SQLAlchemy y Pydantic

# ----------------
# SCHEMAS PYDANTIC - TASKS 
# ----------------

class LoginRequest(BaseModel):
    username: str
    password: str

