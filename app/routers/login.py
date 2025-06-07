from fastapi import APIRouter, Depends, HTTPException, status           # APIRouter para definir rutas, Depends para inyección de dependencias
from sqlalchemy.orm import Session                                      # Session para manejar la sesión de la base de datos
import app.models  as models                                            # Tus modelos de SQLAlchemy (Task)                                       # Tus esquemas de Pydantic (Task, TaskCreate)
from app.auth import create_access_token, pwd_context
from app.database import get_db                                         # Para obtener la sesión de la base de datos
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()      







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