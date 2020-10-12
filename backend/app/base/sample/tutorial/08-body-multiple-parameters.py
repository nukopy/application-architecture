from typing import Any, Dict, List, Optional, Type, TypeVar

from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel
from starlette import responses


T = TypeVar("T", bound="ObjectBase")


class ObjectBase(BaseModel):
    @classmethod
    def create(cls: Type[T], data: Dict[str, Any]) -> T:
        """ Factory method: Create pydantic model from dict """
        return cls(**data)

    def dump(self: T) -> Dict[str, Any]:
        """ Dump pydantic model to dict """
        return self.dict()


class Item(ObjectBase):
    name: str
    description: Optional[str] = None
    price: float


class User(ObjectBase):
    username: str
    full_name: Optional[str] = None


app = FastAPI()


item_list = [
    {"name": "Indian Curry", "price": "1000"},
    {"name": "Coffee", "price": "500"},
    {"name": "Orange Juice", "price": "450"},
]
item_models = [Item.create(item) for item in item_list]


@app.put("/items/{item_id}")
async def get_item(
    item_id: int = Path(..., title="The ID of the item to get", ge=100, le=500),
    q: Optional[str] = Query(None, alias="item-query"),
    item: Item = Body(..., embed=False),
    user: User = Body(..., embed=False),
    # body parameter が 2 つ以上になると embed=False は意味がなくなる
):
    response = {"item_id": item_id}
    if q:
        response.update({"query": q})
    if item:
        response.update({"item": item})
    # if user:
    #     response.update({"user": user})

    return response
