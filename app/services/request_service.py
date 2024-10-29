from datetime import date
from typing import Optional
from app.database import DatabaseManager
from app.exceptions.not_found_error import NotFoundError
from app.models import user_product_points
from app.models.product import Product
from app.models.request import Request
from app.models.request_state import RequestState
from app.schemas.request_schema import RequestIn

class RequestService:
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

    def __prepare_request(self, request):
        return {
            "id": request.id,
            "invoice_id": request.invoice_id,
            "purchase_date": request.purchase_date,
            "product_quantity": request.product_quantity,
            "invoice_image": request.invoice_image,
            "request_state": request.request_state.name,
            "pharmacy": request.pharmacy,
            "user": request.user,
            "product": self.__prepare_product(request.product)
        }
    def __prepare_simple_request(self, request):
        return {
            "id": request.id,
            "invoice_id": request.invoice_id,
            "product_name": request.product.name,
            "request_state": request.request_state.name
        }
    def get_requests(
            self, pharmacy_id: int = None
            ,product_id: int = None
            ,purchase_date: date = None
            ,request_state_id: int = None
            ,user_id: int = None):
        session = next(self.db.get_session())
        requests = session.query(Request)
        if pharmacy_id is not None:
            requests = requests.filter(Request.pharmacy_id == pharmacy_id)
        if product_id is not None:
            requests = requests.filter(Request.product_id == product_id)
        if purchase_date is not None:
            requests = requests.filter(Request.purchase_date == purchase_date)
        if request_state_id is not None:
            requests = requests.filter(Request.request_state_id == request_state_id)
        if user_id is not None:
            requests = requests.filter(Request.user_id == user_id)
        requests = requests.all()
        
        return [self.__prepare_simple_request(request) for request in requests]
    
    def get_request(self, id):
        session = next(self.db.get_session())
        request = session.query(Request).filter(Request.id == id).first()
        if request is None:
            raise NotFoundError("Request not found")
        
        return self.__prepare_request(request)
    
    # Updates the state of a request, if the request is in pending state and the 
    # new state is accepted, the user points are updated
    def update_request_state(self, id, request_state_id):
        session = next(self.db.get_session())
        request = session.query(Request).filter(Request.id == id).first()
        if request is None:
            raise NotFoundError("Request not found")
        if request.product.is_in_program == False:
            raise NotFoundError("Product is not in program")
        new_state = session.query(RequestState).filter(RequestState.id == request_state_id).first()
        if new_state is None:
            raise NotFoundError("Request state not found")
        
        # Logic to update user points
        if request.request_state.name == "Pending" and new_state.name == "Accepted":
            user_points = session.query(user_product_points).filter(
                user_product_points.c.user_id == request.user_id,
                user_product_points.c.product_id == request.product_id).first()
            
            points_to_add = request.product.points_per_purchase * request.product_quantity
            if user_points is None:
                session.execute(user_product_points.insert().values(
                    user_id=request.user_id,
                    product_id=request.product_id,
                    points=points_to_add
                ))
            else:
                session.execute(
                    user_product_points.update()
                    .where(
                        user_product_points.c.user_id == request.user_id,
                        user_product_points.c.product_id == request.product_id
                    )
                    .values(points=user_points.points + points_to_add)
                )
        request.request_state_id = request_state_id
        session.commit()
        session.refresh(request)
        
        return self.__prepare_request(request)
    
    def create_request(self, request: RequestIn):
        session = next(self.db.get_session())
        request = Request(**request.model_dump())
        request_state = session.query(RequestState).filter(RequestState.name == "Pending").first()
        request.request_state_id = request_state.id
        
        session.add(request)
        session.commit()
        session.refresh(request)
        return self.__prepare_request(request)
    