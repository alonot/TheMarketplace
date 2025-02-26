## define pydantic models for requests here

from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, field_validator, model_validator

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RequestSignUp(BaseModel):
    username: str
    password: str
    email: EmailStr
    name: str
    rollno: str

    ## hash the password
    @field_validator("password")
    @classmethod
    def hash_password(cls, value: str) -> str:
        return pwd_context.hash(value)  # Hash the password before storing it

class RequestSignIn(BaseModel):
    username: str | None
    password: str
    email: EmailStr | None

    ## hash the password
    @field_validator("password")
    @classmethod
    def hash_password(cls, value: str) -> str:
        return pwd_context.hash(value)  # Hash the password before storing it
    
    @model_validator(mode="after")
    def validate_model(self):
        if self.username is None and self.email is None:
            raise ValueError("Both username and email cannot be None")
        return self