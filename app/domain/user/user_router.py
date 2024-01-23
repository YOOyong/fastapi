from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_schema, user_crud

router = APIRouter(
    prefix="/api/user",
)


@router.post('/create', status_code=status.HTTP_201_CREATED)
def user_create(_user_create: user_schema.UserCreate,
                db: Session = Depends(get_db)):
    user_crud.create(db, user_info=_user_create)


@router.get('/list', response_model=user_schema.UserList)
def user_list(db: Session = Depends(get_db)):
    user_list = user_crud.get_user_list(db)

    return {
        "user_list": user_list
    }
