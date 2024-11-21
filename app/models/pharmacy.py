from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Pharmacy(Base):
    __tablename__ = "pharmacy"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    schedule: Mapped[str] = mapped_column(String)

    associated_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    associated_user: Mapped["User"] = relationship(back_populates="pharmacy") # type: ignore
    
