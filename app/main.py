from fastapi import FastAPI
from . import schemas # Llamamos a los esquemas definido en schemas.py
from . import database
from . import models # Llamamos a los modelos de SQLAlchemy generado en models.py
from .routers import users, tasks, login
from . import auth

app = FastAPI()

app.include_router(users.router) # Para acceder a las routas contenidas en routes 
app.include_router(tasks.router)
app.include_router(login.router)




if __name__ == '__main__':
    database.Base.metadata.create_all(database.engine) # Creamos la Bd si no lo está ya.
    