
'''
/admin/request/approv
/admin/request/reject
/admin/item/approv
/admin/item/reject
'''

from typing import List
from fastapi import APIRouter, Request

from backend.admin.request_models import IdLists
from backend.admin.response_models import ItemRequestResponse, ItemRequestsResponse, ItemResponse, ItemsResponse
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
