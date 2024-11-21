from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from app.database.base import Base
from app.database.database_manager import DatabaseManager

class Trade(Base):
    __tablename__ = "trade"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"))
    pharmacy_id: Mapped[int] = mapped_column(Integer, ForeignKey("pharmacy.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    date_of_trade: Mapped[date] = mapped_column(Date)

    user: Mapped["User"] = relationship(back_populates="trades") # type: ignore
    product: Mapped["Product"] = relationship() # type: ignore
    pharmacy: Mapped["Pharmacy"] = relationship() # type: ignore
    
    def __repr__(self):
        return f"Trade(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, pharmacy_id={self.pharmacy_id}, quantity"