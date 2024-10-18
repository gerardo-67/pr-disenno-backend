from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.base import Base

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String)
    identification: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean)

    