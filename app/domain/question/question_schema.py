import datetime
from pydantic import BaseModel, field_validator
from typing import List
from domain.answer.answer_schema import Answer

class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: List[Answer] = [] #모델에서 backref 를 설정했기에 가져오기 가능


class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
