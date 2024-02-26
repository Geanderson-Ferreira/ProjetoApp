from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db_manager.config import BASE as Base
import base64


# Define the association table for user access control
user_hotel_association = Table(
    'user_hotel_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.UserId')),
    Column('hotel_id', Integer, ForeignKey('hotels.HotelId'))
)

class Hotel(Base):
    __tablename__ = 'hotels'

    HotelId = Column(Integer, primary_key=True, autoincrement=True)
    HotelName = Column(String, unique=True, nullable=False)
    locations = relationship('Location', back_populates='Hotel')
    orders = relationship('Order', back_populates='Hotel') 

    users = relationship('User', secondary=user_hotel_association, back_populates='hotels')


class LocationType(Base):
    __tablename__ = 'location_types'

    LocationTypeId = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    LocationTypeName = Column(String, nullable=False, unique=True)
    location = relationship('Location', back_populates='LocationTypeName')


class Location(Base):
    __tablename__ = 'locations'

    LocationId = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    LocationTypeId = Column(Integer, ForeignKey('location_types.LocationTypeId', name='fk_location_type', ondelete='CASCADE', deferrable=False), nullable=False)
    LocationName = Column(String, nullable=False)
    Floor = Column(Integer, nullable=False)
    HotelId = Column(Integer, ForeignKey('hotels.HotelId', name='fk_location_hotel', ondelete='CASCADE', deferrable=False))
    
    orders = relationship('Order', back_populates='Location_rel')
    Hotel = relationship('Hotel')
    LocationTypeName = relationship('LocationType', back_populates='location')

class Order(Base):
    __tablename__ = 'orders'

    OrderId = Column(Integer, primary_key=True, autoincrement=True)
    LocationId = Column(Integer, ForeignKey('locations.LocationId', name='fk_location', ondelete='CASCADE', deferrable=False))
    CreationDate = Column(DateTime)
    EndDate = Column(DateTime)
    OrderTypeId = Column(Integer, ForeignKey('order_types.OrderTypeId', name='fk_ordertype', ondelete='CASCADE', deferrable=False))
    ImageData = Column(String, nullable=True)  # Use String for image data
    Description = Column(String)
    UserId = Column(Integer, ForeignKey('users.UserId', name='fk_orderType', ondelete='SET NULL', deferrable=False))
    OrderStatusId = Column(Integer, ForeignKey('order_status.OrderStatusId', name='fk_orderstatus', ondelete='CASCADE', deferrable=False), default=1)
    HotelId = Column(Integer, ForeignKey('hotels.HotelId', name='fk_location_hotel', ondelete='CASCADE', deferrable=False))
    
    Location_rel = relationship('Location', back_populates='orders')
    OrderType = relationship('OrderType', back_populates='orders')
    created_by = relationship('User', back_populates='orders')
    Hotel = relationship('Hotel', back_populates='orders')
    OrderStatus = relationship('OrderStatus', back_populates='orders')

    def set_image_data(self, image_data):
        # Encode binary data to base64 before storing in the database
        self.ImageData = base64.b64encode(image_data).decode('utf-8')

    def get_image_data(self):
        # Decode base64 string when retrieving from the database
        return base64.b64decode(self.ImageData)

class User(Base):
    __tablename__ = 'users'

    UserId = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String, unique=True, nullable=False)
    Password = Column(String, nullable=False, unique=True)
    FullName = Column(String)
    Email = Column(String, unique=True, nullable=False)

    CreatedAt = Column(DateTime, default=datetime.utcnow)
    orders = relationship('Order', back_populates='created_by')
    hotels = relationship('Hotel', secondary=user_hotel_association, back_populates='users')


class OrderType(Base):
    __tablename__ = 'order_types'

    OrderTypeId = Column(Integer, primary_key=True)
    OrderTypeName = Column(String, unique=True, nullable=False)
    orders = relationship('Order', back_populates='OrderType')

class OrderStatus(Base):
    __tablename__ = 'order_status'

    OrderStatusId = Column(Integer, primary_key=True)
    StatusName = Column(String, unique=True, nullable=False)
    orders = relationship('Order', back_populates='OrderStatus')