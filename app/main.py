from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get('/')
async def root():
    return {"message": "Hello World"}


# url에서 파라미터 전달받기.
# @app.get("/items/bugger") 같은 fixed url은 아래 @app.get('/items/{item_id}') 보다 먼저 와야한다.
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get('/users/{user_id}')
async def read_user(user_id: int):
    return {"item_id": user_id}


# url에 정의되지 않은 파라미터는 자동으로 쿼리스트링 값으로 간주된다.
# http://127.0.0.1:8000/items/?skip=1&limit=5
# 쿼리스트링은 string이지만, 아래서 타입을 선언하면 자동으로 캐스팅 해줌.
@app.get('/itemsq/')
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


# 옵셔널 파라미터
# 디폴트를 None 으로 줘서 옵셔널 파라미터로 설정 가능
# 기본값 설정 없으면 필수 쿼리 스트링
@app.get('/items/{item_id}')
async def read_item_option(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# 여러개의 path parameter 가능
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


### REQUEST BODY
class Item(BaseModel):
    # 기본값 없으면 필수임.
    # 기본값 None - 옵셔널
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.post("/create_item/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict


