from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.base import Base

class UserProductPoints(Base):
    __tablename__ = "user_product_points"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    points: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))

    user: Mapped["User"] = relationship(back_populates="product_points")
    product: Mapped["Product"] = relationship()