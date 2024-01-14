from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from domain.question import question_router
from domain.answer import answer_router

app = FastAPI()
app.include_router(question_router.router)
app.include_router(answer_router.router)

@app.get('/')
async def root():
    return {"message": "Hello World"}



