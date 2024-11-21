from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    identification: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean)

    used_points: Mapped[int] = mapped_column(Integer, default=0)
    available_points: Mapped[int] = mapped_column(Integer, default=0)
    total_trades: Mapped[int] = mapped_column(Integer, default=0)

    requests: Mapped[list["Request"]] = relationship(back_populates="user") # type: ignore
    pharmacy: Mapped["Pharmacy"] = relationship(back_populates="associated_user") # type: ignore
    trades: Mapped[list["Trade"]] = relationship(back_populates="user") # type: ignore

    def __init__(self, name: str, email: str, password: str, identification: str, used_points: int = 0, available_points: int = 0, total_trades: int = 0, is_admin: bool = False):
        self.name = name
        self.email = email
        self.password = password
        self.identification = identification
        self.is_admin = is_admin
        self.used_points = used_points
        self.available_points = available_points
        self.total_trades = total_trades
        

    