from app.database import DatabaseManager
from app.exceptions.not_found_error import NotFoundError
from app.models.pharmacy import Pharmacy

class PharmacyService:
    def __init__(self):
        self.db = DatabaseManager()

    def get_pharmacies(self):
        session = next(self.db.get_session())
        pharmacies = session.query(Pharmacy).all()
        
        return pharmacies
    def get_pharmacy(self, id):
        session = next(self.db.get_session())
        pharmacy = session.query(Pharmacy).filter(Pharmacy.id == id).first()
        if pharmacy is None:
            raise NotFoundError("Pharmacy not found")
        
        return pharmacy
    def get_pharmacy_by_name(self, name):
        session = next(self.db.get_session())
        pharmacy = session.query(Pharmacy).filter(Pharmacy.name == name).first()
        if pharmacy is None:
            raise NotFoundError("Pharmacy not found")
        
        return pharmacy
