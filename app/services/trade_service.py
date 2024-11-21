from datetime import date

from fastapi import Depends
from app.database.database_manager import DatabaseManager
from app.exceptions.insufficient_points_error import InsufficientPointsError
from app.exceptions.not_found_error import NotFoundError
from app.models import user_product_points
from app.models.product import Product
from app.models.trade import Trade
from app.services.product_service import ProductService

class TradeService:
    def __init__(self):
        self.db = DatabaseManager()

    def __prepare_trade(self, trade: Trade):
        return {
            "id": trade.id,
            "user": trade.user.name,
            "product": trade.product.name,
            "quantity": trade.quantity,
            "date_of_trade": trade.date_of_trade,
            "points_used": trade.product.points_for_redemption * trade.quantity
        }
    def get_trades(self):
        session = next(self.db.get_session())
        trades = session.query(Trade).all()
        return [self.__prepare_trade(trade) for trade in trades]
    
    def get_trade(self, id):
        session = next(self.db.get_session())
        trade = session.query(Trade).filter(Trade.id == id).first()
        if trade is None:
            raise NotFoundError("Trade not found")
        
        return self.__prepare_trade(trade)
    
    def get_trades_of_user(self, user_id):
        session = next(self.db.get_session())
        trades = session.query(Trade).filter(Trade.user_id == user_id).all()
        return [self.__prepare_trade(trade) for trade in trades]
    
    def register_trade(self, user_id: int, product_id: int , pharmacy_id: int, quantity: int):
        """
        Registers a trade for a user.
        Args:
            user_id (int): The ID of the user making the trade.
            product_id (int): The ID of the product being traded.
            quantity (int): The quantity of the product being traded.
        Returns:
            Trade: The registered trade object.
        """
        session = next(self.db.get_session())
        user_points = session.query(user_product_points).filter(
            user_product_points.c.user_id == user_id,
            user_product_points.c.product_id == product_id).first()

        if user_points is None:
            raise InsufficientPointsError("User does not have points to make this trade")

        product_points_required = session.query(Product).filter(Product.id == product_id).first().points_for_redemption * quantity

        if user_points.points < product_points_required:
            raise InsufficientPointsError("User does not have enough points to make this trade")
        
        trade = Trade(user_id=user_id, pharmacy_id=pharmacy_id, product_id=product_id, quantity=quantity, date_of_trade=date.today())
        session.add(trade)
        session.commit()
        session.refresh(trade)
        used_points = trade.product.points_for_redemption * trade.quantity


        session.execute(
            user_product_points.update()
            .where(
                user_product_points.c.user_id == user_id,
                user_product_points.c.product_id == product_id
            )
            .values(points=user_points.points - used_points)
        )
        trade.user.total_trades += 1
        trade.user.available_points -= used_points
        trade.user.used_points += used_points
        
        session.commit()
        return self.__prepare_trade(trade)
    