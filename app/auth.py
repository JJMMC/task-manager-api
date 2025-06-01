from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import datetime
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database import get_db 
import app.models as models

SECRET_KEY = "superclave"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Para Hashear las contraseñas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # Autenticación de Token
#oauth2_scheme2 = OAuth2PasswordBearer(tokenUrl="token") # Autenticación de Token


def create_access_token(data: dict):
    to_encode = data.copy()
    now = datetime.datetime.now(datetime.timezone.utc)
    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = db.query(models.User).filter(models.User.user_name == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    

