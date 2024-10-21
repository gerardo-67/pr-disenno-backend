from datetime import date
from sqlalchemy import Date, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Request(Base):
    __tablename__ = "request"
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(Integer, index=True)
    purchase_date: Mapped[date] = mapped_column(Date)
    product_quantity: Mapped[int] = mapped_column(Integer)
    invoice_image: Mapped[str] = mapped_column(String)
    request_state_id: Mapped[int] = mapped_column(Integer, ForeignKey("request_state.id"))
    pharmacy_id: Mapped[int] = mapped_column(Integer, ForeignKey("pharmacy.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"))

    request_state: Mapped["RequestState"] = relationship(back_populates="requests") # type: ignore
    pharmacy: Mapped["Pharmacy"] = relationship() # type: ignore
    user: Mapped["User"] = relationship(back_populates="requests") # type: ignore
    product: Mapped["Product"] = relationship() # type: ignore