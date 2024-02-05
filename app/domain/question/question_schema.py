import datetime
from pydantic import BaseModel, field_validator
from domain.answer.answer_schema import Answer
from domain.user.user_schema import User


# 모델은 db와 1대1 대응
# 스키마는 dto 같은 역할을 한다.
# 스키마로 유효성검사 가능
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    modify_date: datetime.datetime | None
    user: User | None
    voter: list[User] = []
    answers: list[Answer] = []  # 모델에서 backref 를 설정했기에 가져오기 가능


class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []


class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class QuestionUpdate(QuestionCreate):
    question_id : int

class QuestionDelete(BaseModel):
    question_id: int


class QuestionVote(BaseModel):
    question_id: int