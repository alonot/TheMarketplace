## define pydantic models for requests here

from pydantic import BaseModel
from typing import List, Optional


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
    title: str
    description: str

class Item(ItemRequest):
    image : Optional[str]

class ItemResponse(Response):
    item: Item

class ItemRequestResponse(Response):
    item: ItemRequest

class ItemsResponse(Response):
    items: List[Item]

class ItemRequestsResponse(Response):
    items: List[ItemRequest]