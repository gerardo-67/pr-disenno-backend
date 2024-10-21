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

    requests: Mapped[list["Request"]] = relationship(back_populates="user") # type: ignore
    
    def __init__(self, name: str, email: str, password: str, identification: str, is_admin: bool = False):
        self.email = email
        self.password = password
        self.name = name
        self.identification = identification
        self.is_admin = is_admin
    