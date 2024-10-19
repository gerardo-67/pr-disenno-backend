from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class ProductForm(Base):
    __tablename__ = "product_form"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    products: Mapped[list["Product"]] = relationship("Product", back_populates="product_form")  # type: ignore