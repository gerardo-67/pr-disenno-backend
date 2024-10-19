from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseManager():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            engine = create_engine('sqlite:///disenno.db')
            cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return cls._instance

    def get_session(self):
        return self.SessionLocal()