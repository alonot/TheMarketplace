## define pydantic models for requests here

from typing import List, Optional
from backend.app.response_models import Response


class AuthResponse(Response):
    access_token: str
    refresh_token: str
