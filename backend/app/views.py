from typing import Optional
from fastapi import APIRouter, Query
from sqlmodel import select
from datetime import timedelta

from backend.admin.request_models import IdLists
from backend.app.utils import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, create_access_token, create_refresh_token
from backend.main import SessionDep
from .models import User
from .request_models import FeedbackRequest, RequestSignUp, RequestSignIn
from .response_models import ItemRequestResponse, ItemRequestsResponse, ItemResponse, ItemsResponse, PaymentsResponse, Response, SignUpResponse, SignInResponse

apirouter = APIRouter()

'''
/login : done
/register : done
/item/<id>
/request/<id>
/item/get_ids : return all the ids of item
/request/get_ids : return all the ids of itemRequests
/item/all?limit=x&page=y&tag=z&name=<contains> : get all the Items. Eg : limit=10&page=0 means return top 10 entries
                                                                           limit=10&page=2 means return top entries from 21th to 30th position [if, assuming 1-indexed sorted array by time]
/request/all?limit=x&page=y&tag=z&name=<contains> : get all the ItemRequests
/user/<id>/payment_method/
/feedback/submit
'''

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


@apirouter.get('/item/all', response_model=ItemsResponse)
async def get_all_items( session: SessionDep, 
    limit: Optional[int] = Query(10, description="Number of items per page"),
    page: Optional[int] = Query(1, description="Page number"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    name: Optional[str] = Query(None, description="Filter by name (Contains)")):
    """
    Get all item with given params
    """
    pass

@apirouter.get('/request/all', response_model=ItemRequestsResponse)
async def get_all_item_requests(  session: SessionDep,
    limit: Optional[int] = Query(10, description="Number of items per page"),
    page: Optional[int] = Query(1, description="Page number"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    name: Optional[str] = Query(None, description="Filter by name (Contains)")):
    """
    Get all itemRequest with given params
    """
    pass

@apirouter.get('/item/get_ids', response_model=IdLists)
async def get_all_items_ids( session: SessionDep):
    """
    Get all item ids 
    """
    pass

@apirouter.get('/request/get_ids', response_model=IdLists)
async def get_all_item_requests_ids(  session: SessionDep):
    """
    Get all itemRequest ids
    """
    pass

@apirouter.get('/request/{id}', response_model=ItemRequestResponse)
async def get_request_info(id: int,  session: SessionDep):
    """
    Get details of a specific item request.
    """
    pass

@apirouter.get('/item/{id}', response_model=ItemResponse)
async def get_item_info(id: int,  session: SessionDep):
    """
    Get details of a specific item request.
    """
    pass


@apirouter.get("/user/{user_id}/payment_methods/", response_model=PaymentsResponse)
def get_payment_methods(user_id: int):
    '''
    returns all the payment methods of a particular user, with its username
    '''
    pass

@apirouter.get('/feedback/submit', response_model=Response)
async def submit_feedback(feedback:FeedbackRequest):
    """
    Get details of a specific item request.
    """
    pass
