from datetime import date, timedelta
import random
from sqlalchemy import DDL, create_engine, text
from dotenv import load_dotenv
import os

from app.database import Base
from app.database.database_manager import DatabaseManager
from app.models import *
from app.models.trade import Trade

# Cargar las variables del archivo .env
load_dotenv()

# Leer la variable de entorno DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

def populate_db():
    session = next(DatabaseManager().get_session())
    
    # Poblar usuarios
    users = []
    for i in range(20):
        if i == 0:
            user = User(
                name='admin',
                email='admin@gmail.com',
                identification='123456789',
                password='123',
                is_admin=True,
                used_points=random.randint(0, 100),
                available_points=random.randint(0, 100),
                total_trades=random.randint(0, 50)
            )
        else:
            user = User(
                name=f'user{i}',
                email=f'user{i}@gmail.com',
                identification=f'{random.randint(100000000, 999999999)}',
                password='123',
                is_admin=False,
                used_points=random.randint(0, 900),
                available_points=random.randint(0, 900),
                total_trades=random.randint(0, 50)
            )
        users.append(user)
    session.add_all(users)
    session.commit()

    # Poblar estados de solicitud
    request_states = [
        RequestState(name='Pending'),
        RequestState(name='Accepted'),
        RequestState(name='Rejected')
    ]
    session.add_all(request_states)
    session.commit()

    # Poblar formas de producto
    product_forms = [
        ProductForm(name='Tablet'),
        ProductForm(name='Capsule'),
        ProductForm(name='Syrup'),
        ProductForm(name='Injection')
    ]
    session.add_all(product_forms)
    session.commit()

    # Poblar farmacias
    pharmacies = [
        Pharmacy(name='Farmacia San Rafael', email='info@farmaciasanrafael.com', address='Calle 1, San Rafael de Escazú', phone_number='2222-2222', schedule='8:00-20:00', associated_user_id=random.randint(1, 20)),
        Pharmacy(name='Farmacia La Bomba', email='info@farmacialabomba.com', address='Avenida Central, San José', phone_number='2221-1212', schedule='8:00-22:00', associated_user_id=random.randint(1, 20)),
        Pharmacy(name='Farmacia 2000', email='info@farmacia2000.com', address='Avenida 10, San José', phone_number='2256-7890', schedule='8:00-21:00', associated_user_id=random.randint(1, 20)),
        Pharmacy(name='Farmacia Universal', email='info@farmaciauniversal.com', address='Calle 5, Cartago', phone_number='2552-5555', schedule='8:00-20:00', associated_user_id=random.randint(1, 20)),
        Pharmacy(name='Farmacia de la Salud', email='info@farmaciadelasalud.com', address='Calle 8, Alajuela', phone_number='2441-2323', schedule='9:00-21:00', associated_user_id=random.randint(1, 20)),
        Pharmacy(name='Farmacia San José', email='info@farmaciasanjose.com', address='Calle 4, San José', phone_number='2256-1234', schedule='8:00-20:00', associated_user_id=random.randint(1, 20)),
        Pharmacy(name='Farmacia Fischel', email='info@farmaciafischel.com', address='Avenida 2, San José', phone_number='2552-1212', schedule='8:00-22:00', associated_user_id=random.randint(1, 20)),
        Pharmacy(name='Farmacia CR', email='info@farmaciacr.com', address='Calle 3, Heredia', phone_number='2610-1010', schedule='8:00-20:00', associated_user_id=random.randint(1, 20)),
        Pharmacy(name='Farmacia La Nacional', email='info@farmacialanacional.com', address='Avenida 4, San José', phone_number='2221-1234', schedule='8:00-21:00', associated_user_id=random.randint(1, 20)),
        Pharmacy(name='Farmacia Más Salud', email='info@farmaciamassalud.com', address='Calle 15, San José', phone_number='2210-2020', schedule='8:00-22:00', associated_user_id=random.randint(1, 20))
    ]
    session.add_all(pharmacies)
    session.commit()

    # Poblar productos
    products = [
        Product(name='Paracetamol', description='Analgésico y antipirético', price=100, is_in_program=True, points_per_purchase=5, points_for_redemption=10, product_form_id=random.randint(1, 4)),
        Product(name='Ibuprofeno', description='Antiinflamatorio', price=150, is_in_program=True, points_per_purchase=30, points_for_redemption=90, product_form_id=random.randint(1, 4)),
        Product(name='Amoxicilina', description='Antibiótico', price=200, is_in_program=True, points_per_purchase=8, points_for_redemption=16, product_form_id=random.randint(1, 4)),
        Product(name='Jarabe para la tos', description='Alivio para la tos', price=180, is_in_program=True, points_per_purchase=20, points_for_redemption=45, product_form_id=random.randint(1, 4)),
        Product(name='Aspirina', description='Analgésico y antiinflamatorio', price=70, is_in_program=True, points_per_purchase=12, points_for_redemption=34, product_form_id=random.randint(1, 4)),
        Product(name='Vitamina C', description='Suplemento vitamínico', price=120, is_in_program=True, points_per_purchase=4, points_for_redemption=8, product_form_id=random.randint(1, 4)),
        Product(name='Cetirizina', description='Antihistamínico para alergias', price=150, is_in_program=True, points_per_purchase=4, points_for_redemption=8, product_form_id=random.randint(1, 4)),
        Product(name='Omeprazol', description='Antiacido', price=250, is_in_program=True, points_per_purchase=7, points_for_redemption=14, product_form_id=random.randint(1, 4)),
        Product(name='Clonazepam', description='Medicamento para la ansiedad', price=300, is_in_program=True, points_per_purchase=45, points_for_redemption=89, product_form_id=random.randint(1, 4)),
        Product(name='Furosemida', description='Diurético', price=22, is_in_program=True, points_per_purchase=6, points_for_redemption=12, product_form_id=random.randint(1, 4)),
        Product(name='Gliclazida', description='Medicamento para diabetes', price=400, is_in_program=True, points_per_purchase=10, points_for_redemption=20, product_form_id=random.randint(1, 4)),
        Product(name='Metformina', description='Medicamento para diabetes tipo 2', price=180, is_in_program=True, points_per_purchase=43, points_for_redemption=102, product_form_id=random.randint(1, 4)),
        Product(name='Amiodarona', description='Medicamento para arritmias', price=450, is_in_program=True, points_per_purchase=12, points_for_redemption=24, product_form_id=random.randint(1, 4)),
        Product(name='Simvastatina', description='Medicamento para colesterol', price=300, is_in_program=True, points_per_purchase=89, points_for_redemption=300, product_form_id=random.randint(1, 4)),
        Product(name='Sildenafil', description='Medicamento para la disfunción eréctil', price=350, is_in_program=True, points_per_purchase=76, points_for_redemption=209, product_form_id=random.randint(1, 4))
    ]
    session.add_all(products)
    session.commit()

    # Poblar transacciones
    trades = []
    for i in range(50):
        trade = Trade(
            user_id=random.randint(1, 20),
            product_id=random.randint(1, 15),
            pharmacy_id=random.randint(1, 10),
            quantity=random.randint(1, 5),
            date_of_trade=date.today() - timedelta(days=random.randint(0, 365))
        )
        trades.append(trade)
    session.add_all(trades)
    session.commit()

    # Poblar solicitudes
    requests = []
    for i in range(50):
        request = Request(
            invoice_id=random.randint(1000, 9999),
            product_id=random.randint(1, 15),
            purchase_date=date.today() - timedelta(days=random.randint(0, 365)),
            product_quantity=random.randint(1, 10),
            invoice_image=f'invoice_{i}.jpg',
            request_state_id=random.randint(1, 3),
            pharmacy_id=random.randint(1, 10),
            user_id=random.randint(1, 20)
        )
        requests.append(request)
    session.add_all(requests)
    session.commit()

    # Poblar puntos de usuario-producto
    user_product_points_data = []
    existing_combinations = set()
    for i in range(100):
        user_id = random.randint(1, 20)
        product_id = random.randint(1, 15)
        if (user_id, product_id) not in existing_combinations:
            user_product_point = {
                'user_id': user_id,
                'product_id': product_id,
                'points': random.randint(700, 1000)
            }
            user_product_points_data.append(user_product_point)
            existing_combinations.add((user_id, product_id))
    session.execute(user_product_points.insert(), user_product_points_data)
    session.commit()



# delete all data from tables
def delete_data():
    session = next(DatabaseManager().get_session())
    session.query(Request).delete()
    session.query(Trade).delete()
    session.query(Pharmacy).delete()
    session.query(RequestState).delete()
    session.query(user_product_points).delete()
    session.query(Product).delete()
    session.query(ProductForm).delete()
    session.query(User).delete()
    session.commit()

    ddl_statements = [
        DDL("ALTER SEQUENCE request_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE pharmacy_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE request_state_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE product_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE product_form_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE user_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE trade_id_seq RESTART WITH 1;")
    ]

    # Ejecutar cada comando DDL
    for ddl in ddl_statements:
        session.execute(ddl)
    session.commit()

populate_db()
#delete_data()