from fastapi import APIRouter, Depends        # APIRouter para definir rutas, Depends para inyección de dependencias
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




