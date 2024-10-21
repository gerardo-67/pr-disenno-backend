from pydantic import BaseModel
from typing import Optional

class ProductFormOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True
class ProductFormIn(BaseModel):
    name: str

class ProductFormUpdate(BaseModel):
    name: Optional[str] = None