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


class ExtensionEnum(str, Enum):
    png = "png"
    jpg = "jpg"
    jpeg = "jpeg"


class Image(ObjectBase):
    id: UUID5
    url: str
    url_pydantic: HttpUrl
    extension: Literal["png", "jpg", "jpeg"]
    extension_enum: ExtensionEnum
    name: str


class Item(ObjectBase):
    name: str = Field(..., title="item name", max_length=100)
    price: float = Field(
        ...,
        title="The price of the item",
        description="The price must be greater than zero",
        gt=0,
    )
    description: Optional[str] = Field(
        None,
        title="The description of the item",
        description="item の説明",
        max_length=300,
    )
    tax: Optional[float] = None
    tags: Set[str] = []
    image: Optional[List[Image]] = None


class Offer(ObjectBase):
    name: str
    description: Optional[str] = Field(None)
    price: float = Field(..., ge=0, le=100000)
    items: List[Item]


# item
item_list = [
    {"name": "Indian Curry", "price": "1000"},
    {"name": "Coffee", "price": "500"},
    {"name": "Orange Juice", "price": "450"},
]
item_models = [Item.create(item) for item in item_list]

# offer
offer_list = [
    {"name": f"OFFER {i}", "price": 750 * (i), "items": item_list} for i in range(1, 10)
]
offer_models = [Offer.create(offer) for offer in offer_list]


@app.post("/images/multiple")
async def create_multiple_images(images: List[Image]):
    return images


@app.put("/items/{item_id}")
async def get_item(
    item_id: int = Path(..., title="The ID of the item to get", ge=100, le=500),
    q: Optional[str] = Query(None, alias="item-query"),
    item: Item = Body(..., embed=True),
):
    response = {"item_id": item_id}
    if q:
        response.update({"query": q})
    if item:
        response.update({"item": item})

    return response


@app.post("/offers")
async def create_offer(offer: List[Offer]):
    return offer
