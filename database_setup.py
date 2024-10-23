from datetime import date, timedelta
import random
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

from app.database import Base
from app.database.database_manager import DatabaseManager
from app.models import *

# Cargar las variables del archivo .env
load_dotenv()

# Leer la variable de entorno DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)



def populate_db():
    session = DatabaseManager().get_session()
    users = []
    for i in range(20):
        if i == 0:
            user = User(
                name='admin',
                email='admin@gmail.com',
                identification='123456789',
                password='123',
                is_admin=True
            )
        else:
            user = User(
                name=f'user{i}',
                email=f'user{i}@gmail.com',
                identification=f'{random.randint(100000000, 999999999)}',
                password='123',
                is_admin=False
            )
        users.append(user)
    session.add_all(users)
    session.commit()

    request_states = []
    request_states.append(RequestState(name='Pending'))
    request_states.append(RequestState(name='Accepted'))
    request_states.append(RequestState(name='Rejected'))

    session.add_all(request_states)
    session.commit()

    product_forms = []
    product_forms.append(ProductForm(name='Tablet'))
    product_forms.append(ProductForm(name='Capsule'))
    product_forms.append(ProductForm(name='Syrup'))
    product_forms.append(ProductForm(name='Injection'))
    
    session.add_all(product_forms)
    session.commit()

    pharmacies = []
    for i in range(10):
        pharmacy = Pharmacy(
            name=f'pharmacy{i}',
            email=f'pharmacy{i}@gmail.com',
            address=f'address{i}',
            phone_number=f'{random.randint(100000000, 999999999)}',
            schedule='8:00-20:00'
        )
        pharmacies.append(pharmacy)
    session.add_all(pharmacies)
    session.commit()

    products = []
    for i in range(30):
        if i % 2 != 0:
            points = random.randint(1, 200)
            product = Product(
                name=f'product{i}',
                description=f'description{i}',
                price=random.randint(1, 100),
                is_in_program=True,
                points_per_purchase=points,
                points_for_redemption=points*2,
                product_form_id=random.randint(1, 4)
            )
        else:
            product = Product(
                name=f'product{i}',
                description=f'description{i}',
                price=random.randint(1, 100),
                product_form_id=random.randint(1, 4)
            )
        products.append(product)
    session.add_all(products)
    session.commit()

    # Crear solicitudes (requests)
    requests = []
    for i in range(50):
        request = Request(
            invoice_id=random.randint(10000, 99999),
            purchase_date=date.today() - timedelta(days=random.randint(1, 30)),
            product_quantity=random.randint(1, 5),
            invoice_image=b'sampleimagebytes',
            request_state_id=random.randint(1, 3),  # IDs de 'Pending', 'Accepted', 'Rejected'
            pharmacy_id=random.randint(1, 10),  # IDs de las farmacias creadas
            user_id=random.randint(1, 20),  # IDs de los usuarios creados
            product_id=random.randint(1, 30)  # IDs de los productos creados
        )
        requests.append(request)
    session.add_all(requests)
    session.commit()

#populate_db()

# delete all data from tables
def delete_data():
    session = DatabaseManager().get_session()
    session.query(Request).delete()
    session.query(Pharmacy).delete()
    session.query(RequestState).delete()
    session.query(user_product_points).delete()
    session.query(Product).delete()
    session.query(ProductForm).delete()
    session.query(User).delete()
    session.commit()

#delete_data()