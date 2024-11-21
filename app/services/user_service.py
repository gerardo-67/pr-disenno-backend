from app.database import DatabaseManager
from app.exceptions.already_in_db_error import AlreadyInDatabaseError
from app.exceptions.not_found_error import NotFoundError
from app.models.user import User
from app.schemas.user_schema import UserIn
from app.services.product_service import ProductService

class UserService:
    def __init__(self):
        self.db = DatabaseManager()
    
    def __prepare_user(self, user: User):
        product_service = ProductService()
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "identification": user.identification,
            "is_admin": user.is_admin,
            "pharmacy_id": None if user.pharmacy is None else user.pharmacy.id,
            "stats": {
                "used_points": user.used_points,
                "available_points": user.available_points,
                "total_trades": user.total_trades,
                "total_points": user.used_points + user.available_points
            },
            "stats_per_product":{
                **product_service.get_products_stats_of_user(user.id)
            }
        }
    def __prepare_user_simple (self, user: User):
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "identification": user.identification,
            "is_admin": user.is_admin,
            "pharmacy_id": None if user.pharmacy is None else user.pharmacy.id
    }
    def get_users(self):
        session = next(self.db.get_session())
        users = session.query(User).all()
        
        return [self.__prepare_user_simple(user) for user in users]
    
    def get_user(self, id):
        session = next(self.db.get_session())
        user = session.query(User).filter(User.id == id).first()
        if user is None:
            raise NotFoundError("User not found")
        
        return self.__prepare_user(user)
    
    def get_user_by_email(self, email):
        session = next(self.db.get_session())
        user = session.query(User).filter(User.email == email).first()
        if user is None:
            raise NotFoundError("User not found")
        
        return self.__prepare_user_simple(user)
    
    def get_user_by_identification(self, identification):
        session = next(self.db.get_session())
        user = session.query(User).filter(User.identification == identification).first()
        if user is None:
            raise NotFoundError("User not found")
        
        return self.__prepare_user_simple(user)

    def validate_user(self, email, password):
        session = next(self.db.get_session())
        user = session.query(User).filter(User.email == email, User.password == password).first()
        if user is None:
            raise NotFoundError("Email or password incorrect")
        
        return self.__prepare_user_simple(user)
    
    def create_user(self, user: UserIn):
        session = next(self.db.get_session())
        user_in_db = session.query(User).filter(User.email == user.email).first()
        if user_in_db is not None:
            raise AlreadyInDatabaseError("User already exists")
        session = next(self.db.get_session())
        user = User(**user.model_dump())
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return self.__prepare_user_simple(user)
    
    def change_password(self, user_id: int, new_password: str):
        session = next(self.db.get_session())
        user = session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise NotFoundError("User not found")
        user.password = new_password
        session.commit()
        session.refresh(user)
        
        return self.__prepare_user_simple(user)