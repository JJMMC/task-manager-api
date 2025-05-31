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

@router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks/", response_model=list[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@router.get("/tasks/{user_id}")
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put('/tasks/')
def update_task( updated_task: schemas.TaskCreate, task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in updated_task.model_dump().items():
        setattr(task, key, value)
    db.commit()
    return task

@router.delete('/tasks/')
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return db.query(models.Task).all()