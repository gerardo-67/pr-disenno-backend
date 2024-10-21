from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    is_in_program: Mapped[bool] = mapped_column(Boolean)
    points_per_purchase: Mapped[int] = mapped_column(Integer, nullable=True)
    points_for_redemption: Mapped[int] = mapped_column(Integer, nullable=True)
    product_form_id: Mapped[int] = mapped_column(Integer, ForeignKey("product_form.id"))

    product_form: Mapped["ProductForm"] = relationship(back_populates="products") # type: ignore

    def __init__(self, name: str, description: str, price: int, product_form_id: int, is_in_program: bool = False, points_per_purchase: int = None, points_for_redemption: int = None):
        self.name = name
        self.description = description
        self.price = price
        self.product_form_id = product_form_id
        self.is_in_program = is_in_program
        self.points_per_purchase = points_per_purchase
        self.points_for_redemption = points_for_redemption