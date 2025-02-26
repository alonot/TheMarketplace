## all the routes

from fastapi import APIRouter

from .request_models import RequestSignUp
from .response_models import SignUpResponse
from ..main import SessionDep


apirouter = APIRouter()

@apirouter.post('/register', response_model=SignUpResponse)
async def register_user(user: RequestSignUp, session: SessionDep):
    ## example return
    return SignUpResponse(status=200,success= True,message= "")