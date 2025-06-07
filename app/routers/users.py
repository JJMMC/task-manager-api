from fastapi import APIRouter, Depends                                  # APIRouter para definir rutas, Depends para inyección de dependencias
from sqlalchemy.orm import Session                                      # Session para manejar la sesión de la base de datos
import app.schemas as schemas                                           # Tus esquemas de Pydantic (Task, TaskCreate)
from app.database import get_db                                         # Para obtener la sesión de la base de datos
from app.services import users_service


router = APIRouter(prefix="/users", tags=['Users'])                     # Instancia de router para registrar rutas


#########
# USERS #
#########

@router.post("/post/",response_model= schemas.User)
def new_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    return users_service.create_user(db, data)

@router.get("/get/", response_model=list[schemas.User])
def list_users(db: Session = Depends(get_db)):
    return users_service.get_users(db)

@router.get("/get/{user_id}", response_model=schemas.User)
def user_by_id(user_id: int, db: Session = Depends(get_db)):
    return users_service.get_user_by_id(db, user_id)

@router.put('/update/{user_id}', response_model=schemas.User)
def update_user(new_data: schemas.UserCreate, user_id: int, db: Session = Depends(get_db)):
    return users_service.put_user(new_data, db, user_id)

@router.delete('/delete/{user_id}', response_model=list[schemas.User])
def remove_user(user_id: int, db: Session = Depends(get_db)):
    return users_service.delete_user(user_id, db)




##############
# EN PRUEBAS #
##############

# @router.get("/protected-route", tags=["Protected"])
# def protected_route(current_user=Depends(get_current_user)):
#     return {"message": f"Hola, {current_user.name}! con email: {current_user.email}"}



