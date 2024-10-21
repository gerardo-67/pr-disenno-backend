from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

user_product_points = Table(
    'user_product_points', Base.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('product_id', ForeignKey('product.id'), primary_key=True),
    Column('points', Integer)
)