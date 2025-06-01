from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime



# ----------------
# SCHEMAS PYDANTIC - USERS
# ----------------

class UserBase(BaseModel):
    name: str
    surname: str
    user_name: str
    email: EmailStr
    password: str
    disable: bool | None = None

class TaskInUser(BaseModel):
    id: int
    title: str
    done: bool

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    tasks: List[TaskInUser] = []  # Relación uno a muchos
    
    class Config:
        from_attributes = True # Para convertir entre SQLAlchemy y Pydantic


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

    class Config:
        from_attributes = True

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime
    owner: Optional[UserInTask]
    
    class Config:
        from_attributes = True # Para convertir entre SQLAlchemy y Pydantic

# ----------------
# SCHEMAS PYDANTIC - TASKS 
# ----------------

class LoginRequest(BaseModel):
    username: str
    password: str

