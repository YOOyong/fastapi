from datetime import timedelta, datetime

from dns.dnssectypes import Algorithm
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from models import User
from domain.user import user_schema, user_crud
from domain.user.user_crud import pwd_context

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "2178d1691a46a0a5a60181fe6c34c9c496aa6fcaea80ce00c12b69dae1332016"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user",
)


@router.post('/login', response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    # check user and password
    user = user_crud.get_user(db, form_data.username)
    # 로그인 정보 검사
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password',
                            headers={'www-Authenticate': 'Bearer'},
                            )

    # make token
    data = {
        'sub': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }


@router.post('/create', status_code=status.HTTP_201_CREATED)
def user_create(_user_create: user_schema.UserCreate,
                db: Session = Depends(get_db)):
    user_crud.create(db, user_info=_user_create)


@router.get('/list', response_model=user_schema.UserList)
def get_user_list(db: Session = Depends(get_db)):
    user_list = user_crud.get_user_list(db)

    return {
        "user_list": user_list
    }


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user


@router.post('/profile/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def update_profile(user_id: int,
                   user_profile_update: user_schema.UserProfileUpdate,
                   current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    db_profile = user_crud.get_user_profile(db, user_id)
    # db_profile이 없는 케이스는 고려하지 않는다
    if db_profile.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")

    user_crud.update_profile(db, db_profile, user_profile_update)


@router.get('/profile/{username}', response_model=user_schema.UserDetail)
def user_detail(username: str,
                db: Session = Depends(get_db)):

    db_user = user_crud.get_user(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail='없는 유저입니다.')
    db_user_profile = user_crud.get_user_profile(db, db_user.id)

    return user_schema.UserDetail(id=db_user.id, email=db_user.email, username=db_user.username,
                                  profile=user_schema.UserProfile(content=db_user_profile.content))
