
from typing import Optional
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy import select

from backend.app.response_models import Response
from backend.auth.request_models import AuthResponse
from .app.models import User
from .app.utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, decode_access_token, decode_refresh_token
from datetime import datetime, timedelta

from .main import SessionDep

def auth_middleware(app):
    return auth_authenticate

def admin_middleware(app):
    return admin_authenticate

def app_middleware(app):
    return send_response

async def admin_authenticate(request: Request, session: SessionDep, call_next):
    
    request, auth_res = await authenticate(request, session)
    db_user : Optional[User] = request.state.user

    if db_user and db_user.admin_id is None:
        return Response(
            status=401,
            success=False,
            message="The User is not an Admin"
        )
    
    if auth_res.status == 200:
        view_response : AuthResponse = await call_next(request, session)
        view_response.access_token = auth_res.access_token
        view_response.refresh_token = auth_res.refresh_token
        return view_response
    
    return auth_res

async def auth_authenticate(request: Request, session: SessionDep, call_next):
    
    request, auth_res = await authenticate(request, session)

    if auth_res.status == 200:
        view_response : AuthResponse = await call_next(request,session)
        view_response.access_token = auth_res.access_token
        view_response.refresh_token = auth_res.refresh_token
        return view_response
    
    return auth_res

'''
Runs for every request and converts the pydantic model into JSON response with correct status code
'''
async def send_response(request: Request, session: SessionDep, call_next):
    res : Response = await call_next(request, session)
    return JSONResponse (
        status_code= res.status,
        content= res.model_dump() ## creates a dictionary from given class members
    )

async def authenticate(request: Request, session: SessionDep) -> tuple[Request, AuthResponse]:

    access_token = request.headers.get("Authorization")
    refresh_token = request.headers.get("X-Refresh-Token")
    
    # Check existence of refresh token
    if not refresh_token:
        return request, AuthResponse (
            status= 401,
            success= False,
            message= "Missing refresh token"
        )

    # Check existence of access_token
    if not access_token:
        return request, AuthResponse (
            status= 401,
            success= False,
            message= "Missing access token"
        )
    
    # Check Format of access_token in Authorizzation header
    if not access_token.startswith("Bearer "):
        return request, AuthResponse (
            status= 401,
            success= False,
            message= "Invalid access token: 'Bearer ' not found"
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
        return request, AuthResponse (
            status= 401,
            success= False,
            message= f"Invalid access token: {str(e)}"
        )

    try:
        refresh_payload = decode_refresh_token(refresh_token)
        refresh_username = refresh_payload.get("username")
        refresh_expiry = datetime.utcfromtimestamp(refresh_payload.get("expiry"))

        # Check if username field match
        if username != refresh_username:
            return request, AuthResponse (
                status= 401,
                success= False,
                message= f"Username Mismatch in access_token and refresh_token"
            )

    except Exception as e:
        return request, AuthResponse (
            status= 401,
            success= False,
            message= f"Invalid refresh token: {str(e)}"
        )

    # If refresh token is expird
    if refresh_expiry < datetime.utcnow():
        return request, AuthResponse (
            status= 401,
            success= False,
            message= "Refresh token expired"
        )
    
    # Check if the user exist in DB
    statement = select(User).where(User.username == username)
    db_user = session.exec(statement).first()

    if db_user is None:
        return request, AuthResponse (
            status= 401,
            success= False,
            message= "User does not exist"
        )

    # If access token is expired, issue a new one
    if access_expiry < datetime.utcnow():
        access_token = create_access_token(
            data={"username": username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    res = AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

    request.state.user = db_user

    return request, res

