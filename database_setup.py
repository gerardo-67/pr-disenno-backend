from app.database import Base
from app.models import *
from sqlalchemy import create_engine

DATABASE_URL_SQLITE = 'sqlite:///disenno.db'

engine = create_engine(DATABASE_URL_SQLITE, echo=True)
Base.metadata.create_all(bind=engine)



