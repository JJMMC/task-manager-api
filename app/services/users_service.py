# from sqlalchemy.orm import Session
# from .. import models


# def create_user(db: Session, data, pwd_context):
#     email_in_db = db.query(models.User).filter(models.User.email == data.email).first()
#     if email_in_db:
#                 return None, "Email already registered"
#     hashed_pwd = pwd_context.hash(data.password)
#     new_user_data = models.User(**data.model_dump(exclude={"password"}), hashed_password=hashed_pwd)
#     db.add(new_user_data)
#     db.commit()
#     db.refresh(new_user_data)
#     return new_user_data, None


# def get_users(db: Session):
#     return db.query(models.User).all()
    