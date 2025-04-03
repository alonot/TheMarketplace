

from fastapi import APIRouter, Request

from backend.app.models import User
from backend.app.response_models import Response
from backend.auth.request_models import ItemRequest, PayRequest, ItemReqRequest
from backend.auth.response_models import OrderResponse, PaymentResponse, UserResponse, WhoamiResponse
from backend.main import SessionDep

'''
/auth : returns info about user
/auth/pay : records a transaction
/auth/item/upsert : update or insert an Item
/auth/request/upsert : update or insert a request for an item
/auth/payment/info : retrieve info about a payment method
/auth/order/info : retrieve info about a transaction method

*** Further Updates ***
/auth/item/notify_admin 
/auth/request/notify_admin 
***
'''

authrouter = APIRouter()

@authrouter.post('/', response_model=UserResponse)
async def whoami(request: Request, session: SessionDep):
    pass

@authrouter.post('/order/info', response_model=OrderResponse)
async def order_info(request: Request, session: SessionDep):
    pass

@authrouter.post('/payment/info', response_model=PaymentResponse)
async def payment_info(request: Request, session: SessionDep):
    pass

@authrouter.post('/pay', response_model=Response)
async def pay(payment: PayRequest, request: Request, session: SessionDep):
    pass

@authrouter.post('/item/upsert', response_model=Response)
async def item_upsert(item: ItemRequest, request: Request, session: SessionDep):
    '''
        An update to Item will remove the approval of the Item and the Item needs to be approved again
    '''
    pass

@authrouter.post('/request/upsert', response_model=Response)
async def request_upsert(item_request: ItemReqRequest,request: Request, session: SessionDep):
    '''
        An update to ItemRequest will remove the approval of the ItemRequest and the ItemRequest needs to be approved again
    '''
    pass