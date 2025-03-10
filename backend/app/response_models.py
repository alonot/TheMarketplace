## define pydantic models for requests here

from pydantic import BaseModel


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
    username: str | None

# Original?
# class SignInResponse(Response):
#     access_token: str | None
#     username: str | None

class SignUpResponse(Response):
      pass
    