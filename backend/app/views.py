from fastapi import APIRouter
from sqlmodel import select
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from .models import User
from .request_models import RequestSignUp, RequestSignIn
from .response_models import SignUpResponse, SignInResponse
from .utils import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_refresh_token, decode_access_token
from ..main import SessionDep

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

apirouter = APIRouter()

authrouter = APIRouter(prefix="/auth")

from fastapi import APIRouter, Request
from sqlmodel import select
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from ..main import SessionDep
from .models import User
from .utils import decode_access_token, decode_refresh_token, create_access_token

authrouter = APIRouter(prefix="/auth")

@authrouter.middleware("http")
async def authenticate(request: Request, session: SessionDep, call_next):

    access_token = request.headers.get("Authorization")
    refresh_token = request.headers.get("X-Refresh-Token")
    
    # Check existence of refresh token
    if not refresh_token:
        return JSONResponse(
            status_code=401,
            content={
                "success": False, 
                "message": "Missing refresh token"
            }
        )

    # Check existence of access_token
    if not access_token:
        return JSONResponse(
            status_code=401,
            content= {
                "success": False, 
                "message": "Missing access token"
            }
        )
    
    # Check Format of access_token in Authorizzation header
    if not access_token.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content= {
                "success": False, 
                "message": "Invalid access token: 'Bearer ' not found"
            }
        )

    access_token = access_token.split()[1]
    username = None
    access_expiry = None
    refresh_expiry = None
    
    try:
        access_payload = decode_access_token(access_token)
        username = access_payload.get("username")
        access_expiry = datetime.utcfromtimestamp(access_payload.get("expiry"))

    except Exception as e:
        return JSONResponse(
            status_code=401,
            content={
                "success": False, 
                "message": f"Invalid access token: {str(e)}"
            }
        )

    try:
        refresh_payload = decode_refresh_token(refresh_token)
        refresh_username = refresh_payload.get("username")
        refresh_expiry = datetime.utcfromtimestamp(refresh_payload.get("expiry"))

        # Check if username field match
        if username != refresh_username:
            return JSONResponse(
                status_code=401,
                content={
                    "success": False, 
                    "message": f"Username Mismatch in access_token and refresh_token"
                }
            )

    except Exception as e:
        return JSONResponse(
            status_code=401,
            content={
                "success": False, 
                "message": f"Invalid refresh token: {str(e)}"
            }
        )

    # If refresh token is expird
    if refresh_expiry < datetime.utcnow():
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "Refresh token expired",
            }
        )
    
    # Check if the user exist in DB
    statement = select(User).where(User.username == username)
    db_user = session.exec(statement).first()

    if db_user is None:
        return JSONResponse(
            status_code=400,
            content={
                "success": False, 
                "message": "User does not exist"
            }
        )

    # If access token is expired, issue a new one
    if access_expiry < datetime.utcnow():
        new_access_token = create_access_token(
            data={"username": username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Access token refreshed",
                "access_token": new_access_token,
                "refresh_token": refresh_token
            }
        )

    

    return await call_next(request)




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
            refresh_token=None, 
            username=None,
        )

    if user.password !=  db_user.password: 
        return SignInResponse(
            status=400, 
            success=False, 
            message="Invalid password", 
            access_token=None, 
            refresh_token=None,
            username=None,
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(data={"username": db_user.username}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"username": db_user.username}, expires_delta=refresh_token_expires)

    return SignInResponse(
        status=200, 
        success=True, 
        message="Login successful", 
        access_token=access_token, 
        refresh_token=refresh_token,
        username=db_user.username
    )
