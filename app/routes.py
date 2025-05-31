from fastapi import APIRouter, Depends, HTTPException        # APIRouter para definir rutas, Depends para inyección de dependencias
from sqlalchemy.orm import Session           # Session para manejar la sesión de la base de datos
import app.models  as models                              # Tus modelos de SQLAlchemy (Task)
import app.schemas as schemas                               # Tus esquemas de Pydantic (Task, TaskCreate)
from app.database import SessionLocal            # Para obtener la sesión de la base de datos

router = APIRouter()                         # Instancia de router para registrar rutas

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#########
# TASKS #
#########

@router.post("/tasks/", response_model=schemas.Task, tags=['Tasks'])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks/", response_model=list[schemas.Task], tags=['Tasks'])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@router.get("/tasks/{task_id}", response_model=schemas.Task, tags=['Tasks'])
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=schemas.Task, tags=['Tasks'])
def update_task( updated_task: schemas.TaskCreate, task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in updated_task.model_dump().items():
        setattr(task, key, value)
    db.commit()
    return task

@router.delete('/tasks/{task_id}', tags=['Tasks'])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}




#########
# USERS #
#########

@router.post("/users/",response_model= schemas.User, tags=['Users'])
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    user_data = models.User(**data.model_dump())
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data

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



