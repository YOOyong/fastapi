# fastapi
fastapi tutorial

# todo
-[ ] https://wikidocs.net/175950 따라가기
-[ ] https://github.com/tiangolo/full-stack-fastapi-postgresql 를 참고하여 리팩토링 해보기.


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
