from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.user.user_router import get_current_user
from domain.question import question_crud
from models import User

router = APIRouter(
    prefix="/api/answer",
)


@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id: int,
                  _answer_create: answer_schema.AnswerCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    # create answer
    question = question_crud.get_question(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    answer_crud.create_answer(db, question=question,
                              answer_create=_answer_create,
                              user=current_user)


@router.get("/detail/{answer_id}", response_model=answer_schema.Answer)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    answer = answer_crud.get_answer(db, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail='없는 답변입니다.')
    return answer


@router.put("/update/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update: answer_schema.AnswerUpdate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, _answer_update.answer_id)

    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Answer not found")

    if not current_user or current_user.id != db_answer.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="수정 권한이 없습니다.")

    answer_crud.update_answer(db, db_answer, _answer_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete: answer_schema.AnswerDelete, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, _answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Answer not found")
    if not current_user or current_user.id != db_answer.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='삭제권한이 없습니다.')

    answer_crud.delete_answer(db, db_answer)


@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def answer_voter(_answer_vote: answer_schema.AnswerVote, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    db_answer = answer_crud.get_answer(db, _answer_vote.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    answer_crud.vote_answer(db, db_answer, user=current_user)


@router.post('/comment/{answer_id}', status_code=status.HTTP_202_ACCEPTED)
def answer_comment_create(answer_id: int,
                          _answer_comment_create: answer_schema.AnswerCommentCreate,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    answer_crud.create_answer_comment(db, _answer_comment_create, answer_id, current_user)


@router.get('/comment/{answer_id}', response_model=answer_schema.AnswerCommentList)
def answer_comment_list(answer_id: int, db: Session = Depends(get_db)):
    return {'comments': answer_crud.get_answer_comment_list(db, answer_id)}


@router.delete('/comment/{answer_comment_id}', status_code=status.HTTP_204_NO_CONTENT)
def answer_comment_delete(answer_comment_id: int,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    db_answer_comment = answer_crud.get_answer_comment(db, answer_comment_id)
    if not db_answer_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment not found")
    if not current_user or current_user.id != db_answer_comment.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='삭제권한이 없습니다.')
    answer_crud.delete_answer_comment(db, db_answer_comment)
