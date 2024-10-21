from datetime import date
from pydantic import BaseModel
from typing import Optional

class RequestStateOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class RequestStateIn(BaseModel):
    name: str

class RequestStateUpdate(BaseModel):
    name: Optional[str] = None
    