from sqlalchemy.orm import Session
from src.db_manager.models import Hotel
from src.schemas.hotel import HotelSchema
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import status

class HotelMethods:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def insert_location(self, hotel: HotelSchema):
        hotel_to_insert = Hotel(
            HotelName=hotel.hotel_name
        )
        try:
            self.db_session.add(hotel_to_insert)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro de Integridade do Banco. Verifique os dados que esta tentando inserir.',
            )
    def delete_hotel(self, hotel_id: int):
        hotel_to_delete = self.db_session.query(Hotel).filter(Hotel.HotelId == hotel_id).first()
        
        if hotel_to_delete:
            self.db_session.delete(hotel_to_delete)
            self.db_session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Hotel with ID {hotel_id} not found.',
            )