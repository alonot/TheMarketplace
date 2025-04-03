## define pydantic models for requests here

from typing import List

from pydantic import BaseModel


class IdLists(BaseModel):
    ids : List[int]