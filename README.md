# fastapi
fastapi tutorial

# todo
- [ ] https://wikidocs.net/175950 따라가기
  - 작성순서를 외워가며 만들어보자
- [ ] https://github.com/tiangolo/full-stack-fastapi-postgresql 를 참고하여 리팩토링 해보기.
- [ ] frontend 부분은 vue.js 로 작성해보기

# memo

### 명령어
```console
- fastapi 시작
uvicorn main:app --reload
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


- [ ] sqlalchemy에서 n+1 문제 확인하기
  - sqlalchemy model에서 lazy = select 일 때,  pydantic 스키마에 정의되어있지 않으면 추가적인 쿼리를 실행하지 않는지