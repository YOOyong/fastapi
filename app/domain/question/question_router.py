from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from models import User
from starlette import status

router = APIRouter(
    prefix="/api/question"
)


@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10, keyword: str = ''):
    # depends 는 매개변수로 받은 함수의 실행 결과를 리턴. 이를 엔드포인트에 매개변수로 전달하여 주입

    total, _questions_list = question_crud.get_question_list(db, skip=page * size, limit=size, keyword=keyword)
    return {
        'total': total,
        'question_list': _questions_list
    }


@router.get('/{question_id}', response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question


@router.post("/create", status_code=status.HTTP_201_CREATED)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question_crud.create_question(db, _question_create, current_user)


@router.put('/update', status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    question_crud.update_question(db=db, db_question=db_question, question_update=_question_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    question_crud.delete_question(db=db, db_question=db_question)


@router.post('/vote', status_code=status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: question_schema.QuestionVote,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='없는 질문입니다.')

    question_crud.vote_question(db=db, db_question=db_question, user=current_user)


@router.get('/comment/{question_id}', response_model=question_schema.QuestionCommentList)
def get_question_comments(question_id: int,
                          db: Session = Depends(get_db)):
    return {'comments': question_crud.get_question_comment_list(db, question_id)}


@router.post('/comment/{question_id}', status_code=status.HTTP_201_CREATED)
def question_comment_create(question_id: int,
                            _question_comment_create: question_schema.QuestionCommentCreate,
                            db: Session = Depends(get_db),
                            current_user: User = Depends(get_current_user)):
    question_crud.create_question_comment(db, _question_comment_create, question_id, current_user)


@router.delete('/comment/{question_comment_id}', status_code=status.HTTP_204_NO_CONTENT)
def question_comment_delete(question_comment_id: int,
                            db: Session = Depends(get_db),
                            current_user: User = Depends(get_current_user)):
    question_comment = question_crud.get_question_comment(db, question_comment_id)
    if not question_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='없는 코멘트 입니다.')
    if not current_user or current_user.id != question_comment.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='삭제권한이 없습니다.')

    question_crud.delete_question_comment(db, question_comment)
