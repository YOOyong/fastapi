from models import Question, Answer, User
from domain.answer import answer_schema
from sqlalchemy.orm import Session
from datetime import datetime


def create_answer(db: Session, question: Question,
                  answer_create: answer_schema.AnswerCreate,
                  user: User):
    db_answer = Answer(question=question,
                       content= answer_create.content,
                       create_date=datetime.now(),
                       user=user)
    db.add(db_answer)
    db.commit()


# def get_answer(db: Session, )