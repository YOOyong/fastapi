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
- [ ] delete 만들때 id 값을 꼭 pydantic 모델로 정의 해야하나?
       그냥 하면 되긴 한느데 문제가 있는건지.
