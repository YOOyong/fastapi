from models import User
from domain.user import user_schema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_list(db: Session):
    return db.query(User).all()


def get_user(db: Session, username:str):
    return db.query(User).filter(User.username == username).first()

def create(db: Session, user_info=user_schema.UserCreate):
    new_user = User(username=user_info.username,
                    email=user_info.email,
                    password=pwd_context.hash(user_info.password1))
    db.add(new_user)
    db.commit()