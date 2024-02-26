from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime
from src.db_manager.models import *
from src.db_manager.config import DATABASE
from src.db_manager.config import BASE as Base
from passlib.context import CryptContext


crypt_context = CryptContext(schemes=['sha256_crypt'])


#Funcao que popula o Banco
def populate():

    engine = create_engine(DATABASE, echo=False)
    Base.metadata.create_all(engine)
    session = Session(engine)

#Dados Aleatorios para preenchimento
    hotel_data = [
        {"HotelName": "Hotel A"},
        {"HotelName": "Hotel B"},
        {"HotelName": "Hotel C"},
        {"HotelName": "Hotel D"},
        {"HotelName": "Hotel E"},
        {"HotelName": "Hotel F"},
        {"HotelName": "Hotel G"},
    ]

    location_types_data = [
        {"LocationTypeName": "Quarto"},
        {"LocationTypeName": "Eventos"},
        {"LocationTypeName": "BackOffice"},
        {"LocationTypeName": "Areas Sociais"},
        {"LocationTypeName": "Fitnes"},
    ]

    location_data = [
        {"LocationTypeId": 1, "LocationName": "752", "Floor": 7, "HotelId": 1},
        {"LocationTypeId": 1, "LocationName": "369", "Floor": 3, "HotelId": 1},
        {"LocationTypeId": 1, "LocationName": "254", "Floor": 2, "HotelId": 1},
        {"LocationTypeId": 2, "LocationName": "Sala de Eventos A", "Floor": 2, "HotelId": 2},
        {"LocationTypeId": 3, "LocationName": "Escritorio", "Floor": 0, "HotelId": 2},
        {"LocationTypeId": 3, "LocationName": "Recepcao", "Floor": 0, "HotelId": 3},
        {"LocationTypeId": 4, "LocationName": "Lobby", "Floor": 0, "HotelId": 1},
    ]

    order_data = [
        {"LocationId": 1, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 1,
        "ImageData": b"sample_image_data", "Description": "Order 1", "UserId": 1, "OrderStatusId": 1, "HotelId": 1},
        {"LocationId": 2, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 2,
        "ImageData": b"sample_image_data", "Description": "Order 2", "UserId": 2, "OrderStatusId": 2, "HotelId": 2},
        {"LocationId": 3, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 3,
        "ImageData": b"sample_image_data", "Description": "Order 3", "UserId": 3, "OrderStatusId": 2, "HotelId": 3},
        {"LocationId": 4, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 4,
        "ImageData": b"sample_image_data", "Description": "Order 4", "UserId": 2, "OrderStatusId": 2, "HotelId": 4},
        {"LocationId": 5, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 5,
        "ImageData": b"sample_image_data", "Description": "Order 5", "UserId": 1, "OrderStatusId": 2, "HotelId": 5},
        {"LocationId": 6, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 6,
        "ImageData": b"sample_image_data", "Description": "Order 6", "UserId": 3, "OrderStatusId": 2, "HotelId": 6},
        {"LocationId": 7, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 6,
        "ImageData": b"sample_image_data", "Description": "Order 7", "UserId": 2, "OrderStatusId": 2, "HotelId": 7},  
        {"LocationId": 1, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 1,
        "ImageData": b"sample_image_data", "Description": "Order 1", "UserId": 1, "OrderStatusId": 1, "HotelId": 1},
        {"LocationId": 2, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 2,
        "ImageData": b"sample_image_data", "Description": "Order 2", "UserId": 2, "OrderStatusId": 2, "HotelId": 2},
        {"LocationId": 3, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 3,
        "ImageData": b"sample_image_data", "Description": "Order 3", "UserId": 3, "OrderStatusId": 2, "HotelId": 3},
        {"LocationId": 4, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 4,
        "ImageData": b"sample_image_data", "Description": "Order 4", "UserId": 2, "OrderStatusId": 2, "HotelId": 4},
        {"LocationId": 5, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 5,
        "ImageData": b"sample_image_data", "Description": "Order 5", "UserId": 1, "OrderStatusId": 2, "HotelId": 5},
        {"LocationId": 6, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 6,
        "ImageData": b"sample_image_data", "Description": "Order 6", "UserId": 3, "OrderStatusId": 2, "HotelId": 6},
        {"LocationId": 7, "CreationDate": datetime.utcnow(), "EndDate": datetime.utcnow(), "OrderTypeId": 6,
        "ImageData": b"sample_image_data", "Description": "Order 7", "UserId": 2, "OrderStatusId": 2, "HotelId": 7},  
]

    user_data = [
        {"Username": "admin", "Password": crypt_context.hash("admin"), "FullName": "Admin", "Email": "admin@admin.com"},
        {"Username": "user2", "Password": crypt_context.hash("password2"), "FullName": "User Two", "Email": "user2@example.com"},
        {"Username": "user3", "Password": crypt_context.hash("password3"), "FullName": "User Three", "Email": "user3@example.com"},
        {"Username": "user4", "Password": crypt_context.hash("password4"), "FullName": "User Four", "Email": "user4@example.com"},
        {"Username": "user5", "Password": crypt_context.hash("password5"), "FullName": "User Five", "Email": "user5@example.com"},
        {"Username": "user6", "Password": crypt_context.hash("password6"), "FullName": "User Six", "Email": "user6@example.com"},
    ]

    order_type_data = [
        {"OrderTypeName": "Pintura"},
        {"OrderTypeName": "Mobilia"},
        {"OrderTypeName": "TV"},
        {"OrderTypeName": "Telefone"},
        {"OrderTypeName": "Frigobar"},
        {"OrderTypeName": "Ar Condicionado"},
        {"OrderTypeName": "Iluminacao"},
        {"OrderTypeName": "Banheiro"},
        {"OrderTypeName": "Outros"},
    ]

    order_status_data = [
        {"StatusName": "Pendente"},
        {"StatusName": "A Bloquear"},
        {"StatusName": "Finalizado"},
    ]

#Insere os dados
    try:

        for hotel in hotel_data:
            session.add(Hotel(**hotel))

        for location in location_data:
            session.add(Location(**location))

        for order in order_data:
            session.add(Order(**order))

        for user in user_data:
            session.add(User(**user))

        for order_type in order_type_data:
            session.add(OrderType(**order_type))

        for order_status in order_status_data:
            session.add(OrderStatus(**order_status))

        for location_type in location_types_data:
            session.add(LocationType(**location_type))

        session.commit()
        session.close()

        print('>> DB POPULADO')
    except Exception as erro:

        print('>> ERRO:\n\n', erro, '\n')
