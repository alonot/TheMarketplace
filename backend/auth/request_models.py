## define pydantic models for requests here

from typing import Optional
from pydantic import BaseModel


class PayRequest(BaseModel):
    transaction_id : str
    answers: dict[str, str]

class ItemRequest(BaseModel):
    item_id: str
    title: Optional[str]
    description: Optional[str]
    image_id: Optional[str]
    image_val: Optional[str]

class ItemReqRequest(BaseModel):
    id: str
    title: Optional[str]
    description: Optional[str]