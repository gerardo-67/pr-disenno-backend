from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from app.exceptions.not_found_error import NotFoundError
from app.schemas.request_schema import RequestOut, RequestIn, RequestStateUpdate, SimpleRequest
from app.services.request_service import RequestService

request_router = APIRouter(prefix="/requests")

@request_router.get("", response_model=List[SimpleRequest], status_code=status.HTTP_200_OK)
def get_requests(
    pharmacy_id: Optional[int] = None, 
    product_id: Optional[int] = None, 
    purchase_date: Optional[date] = None, 
    request_state_id: Optional[int] = None, 
    user_id: Optional[int] = None,
    invoice_id: Optional[int] = None,
    request_service: RequestService = Depends(RequestService)
    ):
    try:
        return request_service.get_requests(pharmacy_id=pharmacy_id, product_id=product_id, purchase_date=purchase_date, request_state_id=request_state_id, user_id=user_id, invoice_id=invoice_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@request_router.get("/{request_id}", response_model=RequestOut, status_code=status.HTTP_200_OK)
def get_request(request_id: int, request_service: RequestService = Depends(RequestService)):
    try:
        return request_service.get_request(request_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@request_router.post("", response_model=RequestOut, status_code=status.HTTP_201_CREATED)
def create_request(request: RequestIn, request_service: RequestService = Depends(RequestService)):
    return request_service.create_request(request)

@request_router.put("/{request_id}/state", response_model=RequestOut, status_code=status.HTTP_200_OK)
def update_request_state(request_id: int, request_state: RequestStateUpdate, request_service: RequestService = Depends(RequestService)):
    try:
        return request_service.update_request_state(request_id, request_state.request_state)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


    
