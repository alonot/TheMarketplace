from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum

default_now = "CURRENT_TIMESTAMP"

class ParentType(str, Enum):
    PAYMENT = "PAYMENT"
    ITEM = "ITEM"
    ANSWER = "ANSWER"

class AnswerField(str, Enum):
    INTEGER = "INTEGER"
    IMG = "IMG"
    STRING = "STRING"

class User(SQLModel, table=True):
    pk: int = Field(primary_key=True)
    email: str = Field(primary_key=True, unique=True)
    username: str = Field(unique=True, nullable=False)
    name: str =  Field()
    rollno: str =  Field(unique=True)
    hostel: str =  Field()
    role: str = Field()
    admin_id: Optional[int] = Field(primary_key=True)
    created_at: str = Field(default=default_now)
    
    payments: List["Payment"] = Relationship(back_populates="user")
    transactions: List["Transaction"] = Relationship(back_populates="user")

class Payment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.pk")
    title: str = Field()   
    description: str = Field()
    approved_by: Optional[int] = Field(default=None, foreign_key="user.admin_id")
    rejected_by: Optional[int] = Field(default=None, foreign_key="user.admin_id")

    approved_admin: Optional["User"] = Relationship(sa_relationship_kwargs={"primaryjoin": "User.admin_id==Item.approved_by"})
    rejected_admin: Optional["User"] = Relationship(sa_relationship_kwargs={"primaryjoin": "User.admin_id==Item.rejected_by"})
    
    user: User = Relationship(back_populates="payments")
    questions_list: List["Question"] = Relationship(back_populates="payment")
    images: List["Image"] = Relationship(back_populates="payment")

class Question(SQLModel, table=True):
    id: int = Field(primary_key=True)
    question: str = Field(nullable=False)
    payment_id: int = Field(foreign_key="payment.id", nullable=False)
    field_type: AnswerField = Field()
    field_len: int = Field()
    
    payment: Payment = Relationship(back_populates="questions_list")
    answers: List["Answer"] = Relationship(back_populates="question")


class Image(SQLModel, table=True):
    id: int = Field(primary_key=True)
    data: bytes = Field()
    parent_id: int = Field(nullable=False)
    parent_type: ParentType = Field(nullable=False)

class Transaction(SQLModel, table=True):
    transaction_id: int = Field(primary_key=True)
    payment_method: int = Field(foreign_key="payment.id")
    user_id: int = Field(foreign_key="user.pk")
    
    user: User = Relationship(back_populates="transactions")
    answers: List["Answer"] = Relationship(back_populates="transaction")

class Answer(SQLModel, table=True):
    id: int = Field(primary_key=True)
    answer: str = Field(nullable=False)
    question_id: int = Field(foreign_key="question.id", nullable=False)
    transaction_id: int = Field(foreign_key="transaction.transaction_id", nullable=False)
    image_answer: Optional[int] = Field(foreign_key="image.id")
    
    question: Question = Relationship(back_populates="answers")
    transaction: Transaction = Relationship(back_populates="answers")
    image: Optional["Image"] = Relationship()
    

class ItemTagLink(SQLModel, table=True):
    item_id: int = Field(foreign_key="item.id", primary_key=True)
    tag_name: str = Field(foreign_key="tag.name", primary_key=True)

class ItemRequestTagLink(SQLModel, table=True):
    item_request_id: int = Field(foreign_key="itemrequest.id", primary_key=True)
    tag_name: str = Field(foreign_key="tag.name", primary_key=True)

class Item(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.pk")
    title: str = Field()
    short_description : str = Field(max_length=20)
    description: str = Field()
    dilevery_type: str = Field()
    created_at: str = Field(default=default_now)
    image_id : Optional[int] = Field(foreign_key="image.id")
    approved_by: Optional[int] = Field(default=None, foreign_key="user.admin_id")
    rejected_by: Optional[int] = Field(default=None, foreign_key="user.admin_id")

    approved_admin: Optional["User"] = Relationship(sa_relationship_kwargs={"primaryjoin": "User.admin_id==Item.approved_by"})
    rejected_admin: Optional["User"] = Relationship(sa_relationship_kwargs={"primaryjoin": "User.admin_id==Item.rejected_by"})

    tags: List["Tag"] = Relationship(back_populates="items", link_model=ItemTagLink)

class ItemRequest(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.pk")
    title: str = Field()
    description: str = Field()
    created_at: str = Field(default=default_now)
    approved_by: Optional[int] = Field(default=None, foreign_key="user.admin_id")
    rejected_by: Optional[int] = Field(default=None, foreign_key="user.admin_id")

    approved_admin: Optional["User"] = Relationship(sa_relationship_kwargs={"primaryjoin": "User.admin_id==Item.approved_by"})
    rejected_admin: Optional["User"] = Relationship(sa_relationship_kwargs={"primaryjoin": "User.admin_id==Item.rejected_by"})

    tags: List["Tag"] = Relationship(back_populates="item_requests", link_model=ItemRequestTagLink)

class Tag(SQLModel, table=True):
    name: str = Field(nullable=False, primary_key=True, unique=True)

    items: List[Item] = Relationship(back_populates="tags", link_model=ItemTagLink)
    item_requests: List[ItemRequest] = Relationship(back_populates="tags", link_model=ItemRequestTagLink)