from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

question_voter = Table(
    'question_voter', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)

)


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, )
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_users")
    # secondary를 정해줌으로써 voter 가 추가되면 question_voter 로 데이터가 들어간다.
    voter = relationship('User', secondary=question_voter, backref='question_voters')
    modify_date = Column(DateTime, nullable=True)


answer_voter = Table(
    'answer_voter', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key=True)
)


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    # answer 에서 question 모델을 참조하기 위해 넣은 변수.
    # answer.question.subject 식으로 접근 가능하게 해준다.
    question = relationship("Question", backref="answers")  # backref 로 역참조가 가능하게 설정.
    voter = relationship('User', secondary=answer_voter, backref='answer_voters')
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    modify_date = Column(DateTime, nullable=True)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False)
    user = relationship("User", backref="profile")
    content = Column(Text, nullable=True)


# question, answer 모두에 댓글을 달 수 있어야 한다.
# 따로 만드는게 낫겠다.
class QuestionComment(Base):
    __tablename__ = "question_comment"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_comment_users")
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="comments")
    create_date = Column(DateTime, nullable=False)


class AnswerComment(Base):
    __tablename__ = "answer_comment"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_comment_users")
    answer_id = Column(Integer, ForeignKey("answer.id"))
    answer = relationship('Answer', backref='comments')
    create_date = Column(DateTime, nullable=False)
