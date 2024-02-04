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
    question_id: int


class AnswerUpdate(AnswerCreate):
    answer_id: int

# #answer 에서는 pydantic을 사용하지 않고 그냥 해보자
# class AnswerDelete(BaseModel):
#     Answer_id: int
