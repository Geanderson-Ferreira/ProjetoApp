from sqlalchemy.orm import Session
from src.db_manager.models import User, Hotel
from src.schemas.user import UserSchema, UserSchemaForLogin
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import status
from datetime import datetime, timedelta
from src.db_manager.config import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

crypt_context = CryptContext(schemes=['sha256_crypt'])

class UserMethod:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def register_user(self, user: UserSchema):
        user_to_insert = User(
            Username=user.username,
            Password=crypt_context.hash(user.password),
            FullName=user.fullname,
            Email=user.email
        )
        
        try:
            self.db_session.add(user_to_insert)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User Data Already Exists'
            )
    
    def user_login(self, user: UserSchemaForLogin, min_to_expire: int = 30):
        user_on_db = self.db_session.query(User).filter_by(Username=user.username).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username or Password Invalid."
            )
        
        if not crypt_context.verify(user.password, user_on_db.Password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username or Password Invalid."
            )
        
        exp = datetime.utcnow() + timedelta(minutes=min_to_expire)

        payload = {
            'sub' : user.username,
            'exp' : exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

        return {'access_token' : access_token,
                'exp' : exp.isoformat() 
        }

    def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token"
            )
        
        user_on_db = self.db_session.query(User).filter_by(Username=data['sub']).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token"
            )

    def hotel_assignment(self, user_id : int, hotel_id : int):
        user = self.db_session.query(User).filter_by(UserId=user_id).first()
        hotel = self.db_session.query(Hotel).filter_by(HotelId=hotel_id).first()

        if not hotel in user.hotels:
            user.hotels.append(hotel)
            self.db_session.commit()

        user = self.db_session.query(User).filter_by(UserId=user_id).first()

        for i in user.hotels: print(i)

    def remove_hotel_assignment(self, user_id: int, hotel_id: int):
        try:
            user = self.db_session.query(User).filter_by(UserId=user_id).first()
            hotel = self.db_session.query(Hotel).filter_by(HotelId=hotel_id).first()

            if user is None or hotel is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User or Hotel not found"
                )

            if hotel not in user.hotels:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User does not have access to this hotel"
                )

            user.hotels.remove(hotel)
            self.db_session.commit()

            user = self.db_session.query(User).filter_by(UserId=user_id).first()

            return {'message': f"Access to {hotel.HotelName} removed for user {user.Username}"}

        except IntegrityError:
            self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to remove hotel assignment"
            )