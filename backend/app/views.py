from fastapi import APIRouter
from sqlmodel import select
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from .models import User
from .request_models import RequestSignUp, RequestSignIn
from .response_models import SignUpResponse, SignInResponse
from .utils import get_password_hash, verify_password, create_access_token
from ..main import SessionDep

ACCESS_TOKEN_EXPIRE_MINUTES = 30

apirouter = APIRouter()

@apirouter.post('/register', response_model=SignUpResponse)
async def register_user(user: RequestSignUp, session: SessionDep):
    statement = select(User).where(User.username == user.username)
    db_user = session.exec(statement).first()

    if db_user is not None:
        return SignUpResponse(
            status=400, 
            success=False, 
            message="Username already exists"
        )

    user_model = User(
        username=user.username, 
        email=user.email,
        password=user.password, #already hashed ig
        name=user.name,
        rollno=user.rollno,
    )
    
    session.add(user_model)
    session.commit()
    session.refresh(user_model)

    return SignUpResponse(
        status=200, 
        success=True, 
        message="User registered successfully"
    )


@apirouter.post('/login', response_model=SignInResponse)
async def login_user(user: RequestSignIn, session: SessionDep):
    statement = select(User).where(User.username == user.username) if user.username else select(User).where(User.email == user.email)
    db_user = session.exec(statement).first()

    if db_user is None:
        return SignInResponse(
            status=400, 
            success=False, 
            message="User does not exist", 
            access_token=None, 
            username=None,
        )

    if user.password !=  db_user.password: 
        return SignInResponse(
            status=400, 
            success=False, 
            message="Invalid password", 
            access_token=None, 
            username=None,
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)

    return SignInResponse(
        status=200, 
        success=True, 
        message="Login successful", 
        access_token=access_token, 
        username=db_user.username
    )
