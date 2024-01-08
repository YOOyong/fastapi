from fastapi import APIRouter, Depends, Response
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from domain.question import question_schema, question_crud
from models import Question
from starlette import status

router = APIRouter(
    prefix="/api/question"
)


@router.get("/list", response_model=List[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    # depends 는 매개변수로 받은 함수의 실행 결과를 리턴. 이를 엔드포인트에 매개변수로 전달하여 주입
    _questions_list = question_crud.get_question_list(db)
    return _questions_list


# @router.post("create")
# def question_create(db: Session = Depends(get_db)):
#     return Response('', status_code=status.HTTP_201_CREATED)