from models import Question, User, Answer, QuestionComment
from domain.question import question_schema
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime


def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    # 페이징 추가
    # # skip 조회한 데이터의 시작, limit 가져올 개수
    # 검색 추가.
    question_list = db.query(Question)
    if keyword:
        search = '%%%{}%%'.format(keyword)
        sub_query = db.query(Answer.question_id, Answer.content, User.username) \
            .outerjoin(User, and_(Answer.user_id == User.id)).subquery()

        question_list = question_list \
            .outerjoin(User) \
            .outerjoin(sub_query, and_(sub_query.c.question_id == Question.id)) \
            .filter(Question.subject.ilike(search) |
                    Question.content.ilike(search) |
                    User.username.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    sub_query.c.username.ilike(search)
                    )
    total = question_list.distinct().count()
    question_list = question_list.order_by(Question.create_date.desc()) \
        .offset(skip).limit(limit).distinct().all()

    return total, question_list


def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    if question.view_count:
        question.view_count += 1
    else:
        question.view_count = 1  #view_count 추가 전 등록했던 글을 위한 분기. 테스트용
    db.commit()
    return question


def create_question(db: Session,
                    question_create: question_schema.QuestionCreate,
                    user: User):
    db_question = Question(subject=question_create.subject,
                           content=question_create.content,
                           create_date=datetime.now(),
                           view_count=0,
                           user=user)
    db.add(db_question)
    db.commit()


def update_question(db: Session,
                    db_question: Question,
                    question_update: question_schema.QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db.add(db_question)
    db.commit()


def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()


def vote_question(db: Session, db_question: Question, user: User):
    db_question.voter.append(user)
    db.commit()


def create_question_comment(db: Session, question_comment: question_schema.QuestionCommentCreate,
                            question_id: int,
                            user: User):
    db_question_comment = QuestionComment(
        content=question_comment.content,
        question_id=question_id,
        create_date=datetime.now(),
        user=user
    )
    db.add(db_question_comment)
    db.commit()


def get_question_comment(db:Session, question_comment_id: int):
    return db.query(QuestionComment).get(question_comment_id)


def get_question_comment_list(db: Session, question_id: int):
    return db.query(QuestionComment).filter(QuestionComment.question_id == question_id).all()


def delete_question_comment(db:Session, question_comment: QuestionComment):
    db.delete(question_comment)
    db.commit()
