import uuid
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
    item_id: uuid.UUID = Field(...)
    name: str = Field(..., min_length=8)
    price: float = Field(..., ge=0, example=35.4)
    description: Optional[str] = Field(None, example="A very nice Item")
    tax: Optional[float] = Field(None, ge=0, example=3.2)

    class Config:
        schema_extra = {
            "example": {
                "item_id": uuid.uuid5(name="hoge"),
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
    item: Item = Body(..., embed=True,),
):
    response = {"item_id": item_id, "item": item}
    if q:
        response.update({"query": q})

    return response
