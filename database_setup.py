from datetime import date, timedelta
import random
from app.database import Base
from app.database.database_manager import DatabaseManager
from app.models import *
from sqlalchemy import create_engine, insert

DATABASE_URL_SQLITE = 'sqlite:///disenno.db'

engine = create_engine(DATABASE_URL_SQLITE, echo=True)
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

        # Recuperar usuarios y productos de la base de datos
    users = session.query(User).all()
    products = session.query(Product).all()

    # Lista para almacenar los datos que se insertarán
    user_product_points_list = []

    for user in users:
        # Asignar puntos aleatorios para una cantidad aleatoria de productos
        num_products = random.randint(1, len(products))  # Seleccionar un número aleatorio de productos para cada usuario
        selected_products = random.sample(products, num_products)  # Seleccionar productos aleatorios

        for product in selected_products:
            points = random.randint(50, 400)  # Asignar una cantidad aleatoria de puntos entre 1 y 100

            # Crear una entrada en la tabla de asociación
            user_product_point_entry = {
                'user_id': user.id,
                'product_id': product.id,
                'points': points
            }
            user_product_points_list.append(user_product_point_entry)

    # Insertar múltiples registros en la tabla de asociación
    session.execute(user_product_points.insert(), user_product_points_list)
    session.commit()


    
populate_db()