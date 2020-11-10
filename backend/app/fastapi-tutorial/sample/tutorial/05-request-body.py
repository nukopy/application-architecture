from typing import Any, Dict, Optional, Type, TypeVar

from fastapi import FastAPI
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
async def get_item():
    return item_models


@app.get("/items/total-price")
async def total_price():
    total_price = sum([item.total_price() for item in item_models])
    return {
        "items": item_models,
        "total_price": total_price,
        "tax_ratio": ItemConfig.TAX_RATIO,
    }


@app.post("/items")
async def create_item(item: Item):
    return item


@app.post("/items/add-2-items")
async def create_2item(item: Item, item2: Item):
    return {
        "id": 1,
        "description": "複数の pydantic モデルを受け取るための例",
        "item 1": item,
        "item 2": item2,
    }
