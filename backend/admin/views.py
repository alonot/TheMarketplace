
'''
/admin/request/approv
/admin/request/reject
/admin/item/reject
/admin/item/approv
/admin/payment_method/approv
/admin/payment_method/reject
/admin/payment_method/all?unapproved=<True/False>&rejected=<True/False> : returns description, title and id of all the payment methods
by default all the requested resource is returned If no query
/admin/request/all?unapproved=<True/False>&rejected=<True/False : returns description, title and id of all the description methods
/admin/item/all?unapproved=<True/False>&rejected=<True/False : returns short_description, title and id of all the items methods
'''
from typing import List, Optional
from fastapi import APIRouter, Query, Request

from backend.admin.request_models import IdLists
from backend.admin.response_models import ItemRequestResponse, ItemResponse, PaymentMethodResponse
from backend.app.response_models import Response
from backend.main import SessionDep

adminrouter = APIRouter()

@adminrouter.post('/request/approve', response_model=Response)
async def approve_request(request_ids: IdLists, request: Request, session: SessionDep):
    """
    Approve all requests given in request_ids.
    """
    pass

@adminrouter.post('/request/reject', response_model=Response)
async def reject_request(request_ids: IdLists, request: Request, session: SessionDep):
    """
    Reject all requests given in request_ids.
    """
    pass

@adminrouter.post('/item/approve', response_model=Response)
async def approve_item(item_ids: IdLists, request: Request, session: SessionDep):
    """
    Approve all items given in item_ids.
    """
    pass

@adminrouter.post('/item/reject', response_model=Response)
async def reject_item(item_ids: IdLists, request: Request, session: SessionDep):
    """
    Reject all items given in item_ids.
    """
    pass

@adminrouter.post('/payment/approve', response_model=Response)
async def approve_item(item_ids: IdLists, request: Request, session: SessionDep):
    """
    Approve all items given in item_ids.
    """
    pass

@adminrouter.post('/payment/reject', response_model=Response)
async def reject_item(item_ids: IdLists, request: Request, session: SessionDep):
    """
    Reject all items given in item_ids.
    """
    pass

@adminrouter.get("/admin/payment_method/all", response_model=List[PaymentMethodResponse])
def get_all_payment_methods(
    unapproved: Optional[bool] = Query(None),
    rejected: Optional[bool] = Query(None)
):
    pass

@adminrouter.get("/admin/request/all", response_model=List[ItemRequestResponse])
def get_all_requests(
    unapproved: Optional[bool] = Query(None),
    rejected: Optional[bool] = Query(None)
):
    pass

@adminrouter.get("/admin/item/all", response_model=List[ItemResponse])
def get_all_items(
    unapproved: Optional[bool] = Query(None),
    rejected: Optional[bool] = Query(None)
):
    pass