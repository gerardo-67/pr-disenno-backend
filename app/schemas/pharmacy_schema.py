from pydantic import BaseModel
from typing import Optional

class PharmacyOut(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str
    address: str
    schedule: str
    class Config:
        from_attributes = True

class PharmacyIn(BaseModel):
    name: str
    email: str
    phone_number: str
    address: str
    schedule: str

class PharmacyUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    schedule: Optional[str] = None
    