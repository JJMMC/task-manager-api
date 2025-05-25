from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import database

app = FastAPI()


# Modelos de pydantic de Validación de datos que vamos a utilizar:

class UserSchema(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    password: str
    disable: bool | None = None

class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    created_at: str
    done: bool | None = None




@app.get('/')
def index():
    print('Hello')

app.post('/task')
def create_task():
    pass


if __name__ == '__main__':
    database.Base.metadata.create_all(database.engine)
