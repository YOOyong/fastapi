from datetime import timedelta, datetime

from dns.dnssectypes import Algorithm
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_schema, user_crud
from domain.user.user_crud import pwd_context

ACCESS_TOKEN_EXPIRE_MINUTES =60 * 24
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

    #make token
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
def user_list(db: Session = Depends(get_db)):
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





