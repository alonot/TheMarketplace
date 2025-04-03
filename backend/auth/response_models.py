## define pydantic models for requests here

from typing import List, Optional
from backend.app.response_models import Response


class AuthResponse(Response):
    access_token: str
    refresh_token: str


class PaymentMethod:
    id : int
    title : str
    description: str

class Order:
    transaction_id: int
    payment_method : int
    user_id: int

class UserResponse(Response):
    email: str
    username: str
    name: str
    rollno: str
    role: str
    admin_id: Optional[int]

    payment_methods: List[PaymentMethod]
    orders: List[Order] 

class OrderResponse(Response, Order):
    answers: List[str] ## all type of answers images, int, or string will be sent to frontend as str

class PaymentResponse(Response, PaymentMethod):
    questions: List[str] ## list of questions
    images: List[str]
