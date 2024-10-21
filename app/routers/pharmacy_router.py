from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app.exceptions.not_found_error import NotFoundError
from app.schemas.pharmacy_schema import PharmacyOut
from app.services.pharmacy_service import PharmacyService

pharmacy_router = APIRouter(prefix="/pharmacies")

def get_service():
    return PharmacyService()

@pharmacy_router.get("", response_model=List[PharmacyOut], status_code=status.HTTP_200_OK)
def get_pharmacies(pharmacy_service: PharmacyService = Depends(get_service)):
    try:
        return pharmacy_service.get_pharmacies()
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@pharmacy_router.get("/{pharmacy_id}", response_model=PharmacyOut, status_code=status.HTTP_200_OK)
def get_pharmacy(pharmacy_id: int, pharmacy_service: PharmacyService = Depends(get_service)):
    try:
        return pharmacy_service.get_pharmacy(pharmacy_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@pharmacy_router.get("/by-name/{pharmacy_name}", response_model=PharmacyOut, status_code=status.HTTP_200_OK)
def get_pharmacy(pharmacy_name: str, pharmacy_service: PharmacyService = Depends(get_service)):
    try:
        return pharmacy_service.get_pharmacy_by_name(pharmacy_name)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))




