from models import User, Profile
from domain.user import user_schema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_list(db: Session):
    # 유저 등록 확인용
    return db.query(User).all()


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create(db: Session, user_info=user_schema.UserCreate):
    new_user = User(username=user_info.username,
                    email=user_info.email,
                    password=pwd_context.hash(user_info.password1))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 유저 생성시 프로필도 함께 생성
    new_profile = Profile(user_id=new_user.id)
    db.add(new_profile)
    db.commit()


def get_user_profile(db: Session, user_id: int):
    return db.query(Profile).filter(Profile.user_id == user_id).first()


def update_profile(db: Session, db_user_profile: Profile, user_profile_update: user_schema.UserProfileUpdate):
    db_user_profile.content = user_profile_update.content
    db.add(db_user_profile)
    db.commit()
