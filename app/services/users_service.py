from sqlalchemy.orm import Session
from fastapi import HTTPException
import app.models as models
import app.schemas as schemas
from app.auth import pwd_context


def create_user(db: Session, user_data: schemas.UserCreate):
    email_in_db = db.query(models.User).filter(models.User.email == user_data.email).first()
    if email_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = pwd_context.hash(user_data.password)
    new_user = models.User(**user_data.model_dump(exclude={"password"}), hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_users(db: Session):
    return db.query(models.User).all()

def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def put_user(new_data: schemas.UserCreate, db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    for key, value in new_data.model_dump().items():
        setattr(user, key, value)
    db.commit()
    return user

def delete_user(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    db.delete(user)
    db.commit()
    return db.query(models.User).all()

