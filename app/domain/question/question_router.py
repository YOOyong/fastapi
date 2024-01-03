from fastapi import APIRouter

from database import SessionLocal
from models import Question

router = APIRouter(
    prefix="/api/question"
)

@router.get("/list")
def question_list():
    db = SessionLocal()
    _questions_list = db.query(Question).order_by(Question.create_date.desc()).all()
    db.close() # 세션을 종료하는것이 아니라 커넥션 풀에 반납하는것.

    return _questions_list



