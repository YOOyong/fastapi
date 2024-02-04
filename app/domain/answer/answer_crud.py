from models import Question, Answer, User
from domain.answer import answer_schema
from sqlalchemy.orm import Session
from datetime import datetime


def create_answer(db: Session, question: Question,
                  answer_create: answer_schema.AnswerCreate,
                  user: User):
    db_answer = Answer(question=question,
                       content=answer_create.content,
                       create_date=datetime.now(),
                       user=user)
    db.add(db_answer)
    db.commit()

def update_answer(db: Session, db_answer: Answer,
                  answer_update:answer_schema.AnswerUpdate):
    db_answer.content = answer_update.content
    db_answer.modify_date = datetime.now()
    db.add(db_answer)
    db.commit()


def get_answer(db: Session, answer_id: int):
    return db.query(Answer).get(answer_id)

def delete_answer(db: Session, db_answer: Answer):
    db.delete(db_answer)
    db.commit()