from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from app.exceptions.already_in_db_error import AlreadyInDatabaseError
from app.exceptions.invalid_input_error import InvalidInputError
from app.exceptions.not_found_error import NotFoundError

from app.schemas.product_schema import ProductOut, ProductIn, ProductProgramIn, SimpleProduct
from app.services.product_service import ProductService

product_router = APIRouter(prefix="/products")

@product_router.get("", response_model=List[SimpleProduct], status_code=status.HTTP_200_OK)
def get_products(is_in_program: Optional[str] = None, product_service: ProductService = Depends(ProductService)):
    try:
        return product_service.get_products(is_in_program)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@product_router.get("/{product_id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
def get_product(product_id: int, product_service: ProductService = Depends(ProductService)):
    try:
        return product_service.get_product(product_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@product_router.get("/by-name/{product_name}", response_model=SimpleProduct, status_code=status.HTTP_200_OK)
def get_product(product_name: str, product_service: ProductService = Depends(ProductService)):
    try:
        return product_service.get_product_by_name(product_name)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@product_router.get("/user/{user_id}", response_model=List[SimpleProduct], status_code=status.HTTP_200_OK)
def get_products_of_user(user_id: int, is_in_program: Optional[bool] = None, product_service: ProductService = Depends(ProductService)):
    try:
        return product_service.get_products_of_user(user_id, is_in_program)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@product_router.post("/{product_id}/program", status_code=status.HTTP_201_CREATED)
def register_product_in_program(product_id: int, program_in: ProductProgramIn, product_service: ProductService = Depends(ProductService)):
    try:
        return product_service.register_product_in_program(product_id, program_in.points_per_purchase, program_in.points_for_redemption)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyInDatabaseError as e:
        raise HTTPException(status_code=409, detail=str(e))
    
