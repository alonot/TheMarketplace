## define pydantic models for requests here


from typing import List
from backend.app.response_models import Response

class PaymentMethodResponse(Response):
    id: int
    title: str

class ItemRequestResponse(Response):
    id: int
    title: str
    description: str
    tag: List[str]

class ItemResponse(Response):
    id: int
    title: str
    short_description: str
    tag: List[str]
    