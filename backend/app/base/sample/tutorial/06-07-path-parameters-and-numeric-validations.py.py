from typing import Any, Dict, List, Optional, Type, TypeVar

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel


T = TypeVar("T", bound="ObjectBase")


class ObjectBase(BaseModel):
    @classmethod
    def create(cls: Type[T], data: Dict[str, Any]) -> T:
        """ Factory method: Create pydantic model from dict """
        return cls(**data)

    def dump(self: T) -> Dict[str, Any]:
        """ Dump pydantic model to dict """
        return self.dict()


class ItemConfig:
    TAX_RATIO: float = 0.10


class Item(ObjectBase):
    name: str
    description: Optional[str] = None
    price: float

    def total_price(self) -> float:
        tax = self.price * ItemConfig.TAX_RATIO
        return self.price + tax


app = FastAPI()


item_list = [
    {"name": "Indian Curry", "price": "1000"},
    {"name": "Coffee", "price": "500"},
    {"name": "Orange Juice", "price": "450"},
]
item_models = [Item.create(item) for item in item_list]


@app.get("/items")
async def get_items(
    q: Optional[str] = Query(..., min_length=3, max_length=50, regex="^[a-z]+$")
):
    response = {"items": item_models}
    if q:
        response.update({"query": q})
    return response


@app.get("/multiple-query")
async def multiple_query(
    q: Optional[List[str]] = Query(
        ...,
        title="List of Query String",
        description='複数のクエリパラメータ "q" を送信することができます．',
        alias="item-query",  # Python の変数名として有効じゃないクエリパラメータ名を alias として使える
        deprecated=True,
    )
):
    query_items = {"q": q}
    return query_items


@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(..., title="The ID of the item to get", ge=100, le=500),
    q: Optional[str] = Query(None, alias="item-query"),
):
    response = {"item_id": item_id}
    if q:
        response.update({"query": q})
    return response
