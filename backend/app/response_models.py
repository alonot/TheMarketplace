## define pydantic models for requests here

from pydantic import BaseModel
from typing import List, Optional

from backend.auth.response_models import PaymentResponse


class Response(BaseModel):
    '''
        This response must be used by all other responses
        i.e. All response must contain these fields
    '''
    status: int
    success: bool
    message: str

class SignInResponse(Response):
    access_token: str | None
    refresh_token: str | None
    username: str | None

# Original?
# class SignInResponse(Response):
#     access_token: str | None
#     username: str | None

class SignUpResponse(Response):
      pass
    


class ItemRequest:
    id: int
    user_id: int
    title: str
    description: str
    tags: List[str]

class Item(ItemRequest):
    short_description : str
    delivery_type: str
    image : List[str]

class ItemResponse(Response):
    item: Item

class ItemRequestResponse(Response):
    items: ItemRequest

class ItemsResponse(Response):
    items: List[Item]

class ItemRequestsResponse(Response):
    items: List[ItemRequest]

class PaymentsResponse(Response, PaymentResponse):
    username: str