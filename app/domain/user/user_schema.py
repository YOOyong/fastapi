import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo

class User(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr


class UserList(BaseModel):
    user_list: list[User] = []


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password1: str
    password2: str

    @field_validator("username", "email","password1","password2")
    def not_empty(cls, v, values):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

    @field_validator('password2')
    def passwords_match(cls, v, info:FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다.')
        return v