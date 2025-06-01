from fastapi import FastAPI
#from pydantic import BaseModel, EmailStr
from app import schemas # Llamamos a los esquemas definido en schemas.py
from app import database
from app import models # Llamamos a los modelos de SQLAlchemy generado en models.py
from app import routes

app = FastAPI()

app.include_router(routes.router) # Para acceder a las routas contenidas en routes 





if __name__ == '__main__':
    database.Base.metadata.create_all(database.engine) # Creamos la Bd si no lo está ya.
    