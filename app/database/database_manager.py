from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# Leer la variable de entorno DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

class DatabaseManager():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            engine = create_engine(
                DATABASE_URL, echo=True)
            cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return cls._instance

    def get_session(self):
        return self.SessionLocal()