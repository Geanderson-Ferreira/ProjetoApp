from sqlalchemy.orm import Session
from src.db_manager.models import LocationType, Location
from src.schemas.location import LocationSchema, LocationTypeSchema
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import status

class LocationMethods:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def insert_location(self, location: LocationSchema):
        location_to_insert = Location(
            LocationTypeId=location.location_type_id,
            LocationName=location.location_name,
            Floor=location.floor,
            HotelId=location.hotel_id
        )
        try:
            self.db_session.add(location_to_insert)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro de Integridade do Banco. Verifique os dados que esta tentando inserir.',
            )
    def delete_location(self, location_id: int):
        location_to_delete = self.db_session.query(Location).filter(Location.LocationId == location_id).first()
        
        if location_to_delete:
            self.db_session.delete(location_to_delete)
            self.db_session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Location with ID {location_id} not found.',
            )
        
    def insert_location_type(self, location_type: LocationTypeSchema):
        location_type_to_insert = LocationType(
            LocationTypeName=location_type.location_type_name
        )
        try:
            self.db_session.add(location_type_to_insert)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Erro de Integridade do Banco. Verifique os dados que esta tentando inserir.',
            )
        
    def delete_location_type(self, location_type_id: int):
        location_type_to_delete = self.db_session.query(LocationType).filter(LocationType.LocationTypeId == location_type_id).first()
        
        if location_type_to_delete:
            self.db_session.delete(location_type_to_delete)
            self.db_session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'LocationType with ID {location_type_id} not found.',
            )