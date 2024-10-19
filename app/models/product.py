from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    is_in_program: Mapped[bool] = mapped_column(Boolean)
    points_per_purchase: Mapped[int] = mapped_column(Integer)
    points_for_redemption: Mapped[int] = mapped_column(Integer)
    product_form_id: Mapped[int] = mapped_column(Integer, ForeignKey("product_form.id"))

    product_form: Mapped["ProductForm"] = relationship(back_populates="products") # type: ignore