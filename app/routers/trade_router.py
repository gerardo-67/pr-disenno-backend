from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.exceptions.insufficient_points_error import InsufficientPointsError
from app.schemas.trade_schema import TradeIn, TradeOut
from app.services.trade_service import TradeService


trade_router = APIRouter(prefix="/trades")

@trade_router.get("", response_model=List[TradeOut], status_code=status.HTTP_200_OK)
def get_trades(trade_service: TradeService = Depends(TradeService)):
    return trade_service.get_trades()

@trade_router.get("/user/{user_id}", response_model=List[TradeOut], status_code=status.HTTP_200_OK)
def get_trades_of_user(user_id: int, trade_service: TradeService = Depends(TradeService)):
    return trade_service.get_trades_of_user(user_id)

@trade_router.get("/{id}", response_model=TradeOut, status_code=status.HTTP_200_OK)
def get_trade(id: int, trade_service: TradeService = Depends(TradeService)):
    try:
        return trade_service.get_trade(id)
    except InsufficientPointsError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@trade_router.post("", response_model=TradeOut, status_code=status.HTTP_201_CREATED)
def register_trade(trade_in: TradeIn, trade_service: TradeService = Depends(TradeService)):
    try:
        return trade_service.register_trade(user_id=trade_in.user_id, product_id=trade_in.product_id, 
                                            pharmacy_id=trade_in.pharmacy_id, quantity=trade_in.quantity)
    except InsufficientPointsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))