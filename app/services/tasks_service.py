from fastapi import HTTPException                   # APIRouter para definir rutas, Depends para inyección de dependencias
from sqlalchemy.orm import Session                                      # Session para manejar la sesión de la base de datos
import app.models  as models                                            # Tus modelos de SQLAlchemy (Task)
import app.schemas as schemas                                           # Tus esquemas de Pydantic (Task, TaskCreate)


def create_task(task: schemas.TaskCreate, db: Session, current_user: models.User):
    db_task = models.Task(**task.model_dump(),user_id = current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_user_tasks(db: Session, current_user: models.User):
    return db.query(models.Task).filter(models.Task.user_id == current_user.id).all()

def get_user_task_by_id(task_id: int, db: Session, current_user: models.User):
    task = db.query(models.Task).filter(models.Task.user_id == current_user.id).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def put_task( updated_task: schemas.TaskCreate, 
                task_id: int, 
                db: Session, 
                current_user: models.User 
                ):
    task = db.query(models.Task).filter(models.Task.user_id == current_user.id).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in updated_task.model_dump().items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(task_id: int, db: Session, current_user: models.User):
    task = db.query(models.Task).filter(models.Task.user_id == current_user.id).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}
