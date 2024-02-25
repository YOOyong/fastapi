# fastapi
fastapi tutorial

# todo
- [ ] https://wikidocs.net/175950 따라가기
- [ ] https://github.com/tiangolo/full-stack-fastapi-postgresql 를 참고하여 리팩토링 해보기.
- [ ] frontend 부분은 vue.js 로 작성해보기
- [ ] Dependency injector 를 사용해 보일러플레이트 참고해 적용, 비교

# memo

### 명령어
```console
- fastapi 시작
uvicorn main:app --reload

- db sqlalchemy model 동기화
-리비전 파일 생성 (테이블 생성, 변경하는 실행문)
  alembic revision --autogenerate 
-리비전 파일 실행
  alembic upgrade head
```



`main`  : 파일명 _main.py_  
`app` : _main.py_ 안에서 만들어진 FastAPI object 명 `app = FastAPI()`


### 문제점
`ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'` 에러.
- 버전문제. 패키지 재설치

### 궁금증
- [x] delete 만들때 id 값을 꼭 pydantic 모델로 정의 해야하나?
  - pydantic 모델을 쓰지 않으면 path varaible 이거나 query string으로 인식됨
  - pydantic 모델을 쓰면 request body 형식임. 
  - id 값과 같은 단일 int 같은건 그냥 쓰는것도 괜찮을 것 같다. ex) get detail
  - 복잡한 유효성 검사가 필요한 경우에는 pydantic 모델을 쓰는것이 낫긴 하다.

- [x] sqlalchemy에서 n+1 문제 확인하기.


- [x] 1 : 1 관계에서 pydantic 모델 작성, 매핑. 
  - answer, user 관계에서 answer 스키마에서 user 스키마를 쓰는건 가능
  - profile, user 관계에서 user 스키마에서 profile 스키마 자동 매핑을 불가능. 왜 이런지 찾아보기.
  - 1 : 1 관계를 설정하는 방법이 잘못되었음. 아래와 같은 형식으로 수정. `uselist=False` 꼭 필요
```python
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child = relationship("Child", uselist=False, backref="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
```