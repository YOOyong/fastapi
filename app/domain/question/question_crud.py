from models import Question
from domain.question import question_schema
from sqlalchemy.orm import Session
from datetime import datetime


def get_question_list(db: Session, skip: int = 0, limit: int = 10):
    # 페이징 추가
    # skip 조회한 데이터의 시작, limit 가져올 개수
    _question_list = db.query(Question).order_by(Question.create_date.desc())
    total = _question_list.count()  # 전체 글 개수
    question_list = _question_list.offset(skip).limit(limit).all()

    return total, question_list


def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question


def create_question(db: Session, question_create: question_schema.QuestionCreate):
    db_question = Question(subject=question_create.subject,
                           content=question_create.content,
                           create_date=datetime.now())
    db.add(db_question)
    db.commit()
