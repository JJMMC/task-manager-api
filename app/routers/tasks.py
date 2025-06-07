from fastapi import APIRouter, Depends                                  # APIRouter para definir rutas, Depends para inyección de dependencias
from sqlalchemy.orm import Session                                      # Session para manejar la sesión de la base de datos
import app.models  as models                                            # Tus modelos de SQLAlchemy (Task)
import app.schemas as schemas                                           # Tus esquemas de Pydantic (Task, TaskCreate)
from app.auth import get_current_user
from app.database import get_db                                         # Para obtener la sesión de la base de datos
from app.services import tasks_service


router = APIRouter(tags=['Tasks'])                                                    # Instancia de router para registrar rutas


#########
# TASKS #
#########

@router.post("/tasks/", response_model=schemas.Task)
def new_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return tasks_service.create_task(task, db, current_user)

@router.get("/tasks/", response_model=list[schemas.Task])
def user_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return tasks_service.get_user_tasks(db, current_user)

@router.get("/tasks/{task_id}", response_model=schemas.Task)
def user_task_by_id(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return tasks_service.get_user_task_by_id(task_id, db, current_user)

@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(updated_task: schemas.TaskCreate, 
                task_id: int, 
                db: Session = Depends(get_db), 
                current_user: models.User = Depends(get_current_user)
                ):
    return tasks_service.put_task(updated_task, task_id, db, current_user,)

@router.delete('/tasks/{task_id}')
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return tasks_service.delete_task(task_id, db, current_user)







