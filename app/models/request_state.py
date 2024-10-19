from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class RequestState(Base):
    __tablename__ = "request_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    requests: Mapped[list["Request"]] = relationship("Request", back_populates="request_state") # type: ignore