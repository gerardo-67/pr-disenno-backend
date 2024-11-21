from datetime import date
from typing import Optional
from pydantic import BaseModel


class TradeIn (BaseModel):
    user_id: int
    product_id: int
    pharmacy_id: int
    quantity: int

class TradeOut (BaseModel):
    id: int
    user: str
    product: str
    quantity: int
    date_of_trade: date
    points_used: int