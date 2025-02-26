## all the database tables

from sqlmodel import Field, SQLModel


class User(SQLModel, table = True):
    username: str = Field(primary_key=True)
    name: str = Field()
    password: str = Field()
    rollno: str = Field(max_length=10, min_length=9) # NOTE: our roll number have 9 digits but still going with 10 digits. Could be changed if all rollnumbers have 9 digits
    email: str = Field() ## email field will be verified via pydantic in request
    ## relationships
    #...