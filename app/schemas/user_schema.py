from pydantic import BaseModel
from typing import Optional

class UserOut(BaseModel):
    id: int
    email: str
    name: str
    identification: str
    is_admin: bool
    class Config:
        from_attributes = True

class UserIn(BaseModel):
    email: str
    name: str
    identification: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    identification: Optional[str] = None
    password: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserPassword(BaseModel):
    user_id: int
    password: str