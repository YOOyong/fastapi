import datetime
from pydantic import BaseModel, field_validator
from domain.user.user_schema import User


class AnswerCreate(BaseModel):
    content: str

    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    modify_date: datetime.datetime | None
    user: User | None
    voter: list[User] = []
    question_id: int


class AnswerUpdate(AnswerCreate):
    answer_id: int


class AnswerVote(BaseModel):
    answer_id: int


class AnswerDelete(BaseModel):
    answer_id: int


class AnswerComment(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    answer_id: int


class AnswerCommentCreate(BaseModel):
    content: str

    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class AnswerCommentList(BaseModel):
    comments: list[AnswerComment] = []
