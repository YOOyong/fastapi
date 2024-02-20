from models import Question, Answer, User, AnswerComment
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
                  answer_update: answer_schema.AnswerUpdate):
    db_answer.content = answer_update.content
    db_answer.modify_date = datetime.now()
    db.add(db_answer)
    db.commit()


def get_answer(db: Session, answer_id: int):
    return db.query(Answer).get(answer_id)


def delete_answer(db: Session, db_answer: Answer):
    db.delete(db_answer)
    db.commit()


def vote_answer(db: Session, db_answer: Answer, user: User):
    db_answer.voter.append(user)
    db.commit()


def create_answer_comment(db: Session,
                          answer_comment_create: answer_schema.AnswerCommentCreate,
                          answer_id: int,
                          user: User):
    answer_comment = AnswerComment(
        content=answer_comment_create.content,
        answer_id=answer_id,
        create_date=datetime.now(),
        user=user
    )
    db.add(answer_comment)
    db.commit()


def delete_answer_comment(db: Session, answer_comment: AnswerComment):
    db.delete(answer_comment)
    db.commit()


def get_answer_comment(db: Session, answer_comment_id: int):
    return db.query(AnswerComment).get(answer_comment_id)


def get_answer_comment_list(db: Session, answer_id: int):
    return db.query(AnswerComment).filter(AnswerComment.answer_id == answer_id).all()
