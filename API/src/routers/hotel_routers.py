from fastapi import APIRouter, Depends, status
from src.schemas.hotel import HotelSchema
from sqlalchemy.orm import Session
from src.db_manager.depends import get_db_session
from src.db_manager.methods.hotel_methods import HotelMethods
from fastapi.responses import JSONResponse
from src.db_manager.config import API_PREFIX
from src.db_manager.depends import token_verifier

router = APIRouter(prefix=API_PREFIX + '/hotel', dependencies=[Depends(token_verifier)])

@router.post('/insert-hotel')
def insert_hotel(hotel: HotelSchema, db_session: Session = Depends(get_db_session)):

    HotelMethods(db_session).insert_location(hotel)

    return JSONResponse(
        content={'msg':'success'},
        status_code=status.HTTP_201_CREATED
    )
@router.post('/delete-hotel')
def delete_hotel(hotel_id: int, db_session: Session = Depends(get_db_session)):
    
    HotelMethods(db_session).delete_hotel(hotel_id)

    return JSONResponse(
        content={'msg':'success'},
        status_code=status.HTTP_201_CREATED
    )