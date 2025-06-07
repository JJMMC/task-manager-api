from fastapi import APIRouter, Depends, HTTPException, status           # APIRouter para definir rutas, Depends para inyección de dependencias
from sqlalchemy.orm import Session                                      # Session para manejar la sesión de la base de datos
import app.models  as models                                            # Tus modelos de SQLAlchemy (Task)
import app.schemas as schemas                                           # Tus esquemas de Pydantic (Task, TaskCreate)
from app.auth import create_access_token, pwd_context, get_current_user
from app.database import SessionLocal, get_db                           # Para obtener la sesión de la base de datos
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users", tags=["users"])                                                    # Instancia de router para registrar rutas





#########
# USERS #
#########

@router.post("/users/",response_model= schemas.User, tags=['Users'])
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    email_in_db = db.query(models.User).filter(models.User.email == data.email).first()
    if email_in_db:
                raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = pwd_context.hash(data.password)
    new_user_data = models.User(**data.model_dump(exclude={"password"}), hashed_password=hashed_pwd)
    db.add(new_user_data)
    db.commit()
    db.refresh(new_user_data)
    return new_user_data

@router.get("/users/", response_model=list[schemas.User], tags=['Users'])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/users/{user_id}", response_model=schemas.User, tags=['Users'])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put('/users/{user_id}', response_model=schemas.User, tags=['Users'])
def update_user( updated_user: schemas.UserCreate, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    for key, value in updated_user.model_dump().items():
        setattr(user, key, value)
    db.commit()
    return user

@router.delete('/users/{user_id}', tags=['Users'])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(user)
    db.commit()
    return db.query(models.User).all()


#########
# TOKEN #
#########

@router.post('/token', tags=['Login'])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_name == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token({"sub": user.user_name})
    return {"access_token": token, "token_type": "bearer"}


##############
# EN PRUEBAS #
##############

@router.get("/protected-route", tags=["Protected"])
def protected_route(current_user=Depends(get_current_user)):
    return {"message": f"Hola, {current_user.name}! con email: {current_user.email}"}



