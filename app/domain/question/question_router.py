from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from domain.question import question_schema, question_crud
from starlette import status

router = APIRouter(
    prefix="/api/question"
)


@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10):
    # depends 는 매개변수로 받은 함수의 실행 결과를 리턴. 이를 엔드포인트에 매개변수로 전달하여 주입

    total, _questions_list = question_crud.get_question_list(db, skip=page * size, limit=size)
    return {
        'total': total,
        'question_list': _questions_list
    }

@router.get('/list/{question_id}', response_model=question_schema.Question)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate, db: Session = Depends(get_db)):
    question_crud.create_question(db, _question_create)
