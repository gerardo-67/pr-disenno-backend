from typing import Optional
from app.database import DatabaseManager
from app.exceptions.already_in_db_error import AlreadyInDatabaseError
from app.exceptions.invalid_input_error import InvalidInputError
from app.exceptions.not_found_error import NotFoundError
from app.models import user_product_points
from app.models.product import Product

class ProductService:
    def __init__(self):
        self.db = DatabaseManager()

    def __prepare_product(self, product: Product, points: Optional[int] = 0):
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "is_in_program": product.is_in_program,
            "points_per_purchase": product.points_per_purchase,
            "points_for_redemption": product.points_for_redemption,
            "product_form": product.product_form.name,
            "points_count": points
        }
    def __prepare_simple_product(self, product: Product, points: Optional[int] = 0):
        return {
            "name": product.name,
            "product_form": product.product_form.name,
            "points_count": points,
            "is_in_program": product.is_in_program
        }
    def get_products(self, is_in_program: Optional[str] = None):
        session = next(self.db.get_session())
        if is_in_program is not None:
            if is_in_program.lower() == "true": 
                products = session.query(Product).filter(Product.is_in_program == True).all()
                return [self.__prepare_product(product) for product in products]
            elif is_in_program.lower() == "false":
                products = session.query(Product).filter(Product.is_in_program == False).all()
                return [self.__prepare_product(product) for product in products]
            else:
                raise InvalidInputError("Invalid input. True or False expected")
        products = session.query(Product).all()
        
        return [self.__prepare_simple_product(product) for product in products]
    
    def get_product(self, id):
        session = next(self.db.get_session())
        product = session.query(Product).filter(Product.id == id).first()
        if product is None:
            raise NotFoundError("Product not found")
        
        return self.__prepare_product(product)

    def get_product_by_name(self, name):
        session = next(self.db.get_session())
        product = session.query(Product).filter(Product.name == name).first()
        if product is None:
            raise NotFoundError("Product not found")
        
        return self.__prepare_simple_product(product)
    
    def get_products_of_user(self, user_id: int, is_in_program: Optional[bool] = None):
        session = next(self.db.get_session())
        products = (
        session.query(Product, user_product_points.c.points)
        .outerjoin(user_product_points, Product.id == user_product_points.c.product_id)
        .filter(user_product_points.c.user_id == user_id)
        )
        if is_in_program is not None:
            products = products.filter(Product.is_in_program == is_in_program)
        
        return [self.__prepare_simple_product(product, points) for product, points in products.all()]
    
    def register_product_in_program(self, product_id: int, points_per_purchase: int, points_for_redemption: int):
        session = next(self.db.get_session())
        product = session.query(Product).filter(Product.id == product_id).first()
        if product is None:
            raise NotFoundError("Product not found")
        if product.is_in_program:
            raise AlreadyInDatabaseError("Product already in program")
        product.is_in_program = True
        product.points_per_purchase = points_per_purchase
        product.points_for_redemption = points_for_redemption
        session.commit()
        
        return self.__prepare_product(product)
