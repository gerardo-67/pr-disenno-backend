from app.database import DatabaseManager
from app.exceptions.already_in_db_error import AlreadyInDatabaseError
from app.exceptions.not_found_error import NotFoundError
from app.models.user import User
from app.schemas.user_schema import UserIn

class UserService:
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_users(self):
        session = self.db.get_session()
        users = session.query(User).all()
        return users
    
    def get_user(self, id):
        session = self.db.get_session()
        user = session.query(User).filter(User.id == id).first()
        if user is None:
            raise NotFoundError("User not found")
        return user
    
    def get_user_by_email(self, email):
        session = self.db.get_session()
        user = session.query(User).filter(User.email == email).first()
        if user is None:
            raise NotFoundError("User not found")
        return user
    
    def validate_user(self, email, password):
        session = self.db.get_session()
        user = session.query(User).filter(User.email == email, User.password == password).first()
        if user is None:
            raise NotFoundError("Email or password incorrect")
        return user
    
    def create_user(self, user: UserIn):
        session = self.db.get_session()
        user_in_db = session.query(User).filter(User.email == user.email).first()
        if user_in_db is not None:
            raise AlreadyInDatabaseError("User already exists")
        session = self.db.get_session()
        user = User(**user.model_dump())
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
    def change_password(self, user_id: int, new_password: str):
        session = self.db.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise NotFoundError("User not found")
        user.password = new_password
        session.commit()
        session.refresh(user)
        return user