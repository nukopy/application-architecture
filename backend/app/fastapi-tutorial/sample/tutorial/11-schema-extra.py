from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Set, Type, TypeVar

from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel, Field, HttpUrl
from pydantic.types import UUID5


app = FastAPI()
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
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., ge=0, example=35.4)
    tax: Optional[float] = Field(None, ge=0, example=3.2)

    # この場合，Config の schema_extra が優先される
    # 自分的にも Config に分離させた方が好みかな
    # TODO: pydantic の使い方として，
    # TODO:・オブジェクト（対象を表す）
    # TODO:・API のリクエスト / レスポンス用のモデル
    # TODO:・ORM 用のモデル（オブジェクトを継承する）
    # TODO: 以上 3 つを別々に定義すれば OK なのでは？
    class Config:
        schema_extra = {
            "example": {
                "name": "Rare Oranges",
                "description": "popular item",
                "price": 33000,
                "tax": 0.8,
            },
        }


@app.put("/items/{item_id}")
async def update_item(
    item_id: int = Path(..., ge=1, le=500),
    q: Optional[str] = Query(None, min_length=3, max_length=50),
    item: Item = Body(
        ...,
        embed=True,
        # request body の話なら Config に書いた方がすっきりすると思う
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    ),
):
    response = {"item_id": item_id, "item": item}
    if q:
        response.update({"query": q})

    return response
