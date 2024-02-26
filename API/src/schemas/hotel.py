from pydantic import BaseModel

class HotelSchema(BaseModel):
    hotel_name : str
