from pydantic import BaseModel
from typing import Optional

from app.schemas.product_form_schema import ProductFormOut

class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: int
    is_in_program: bool
    points_per_purchase: Optional[int] = None
    points_for_redemption: Optional[int] = None
    points_count: Optional[int] = 0
    class Config:
        from_attributes = True

class ProductIn(BaseModel):
    name: str
    description: str
    price: int
    is_in_program: bool
    points_per_purchase: Optional[int] = None
    points_for_redemption: Optional[int] = None
    product_form_id: int

class ProductProgramIn(BaseModel):
    points_per_purchase: int
    points_for_redemption: int


class SimpleProduct(BaseModel):
    name: str
    points_count: int
    is_in_program: bool