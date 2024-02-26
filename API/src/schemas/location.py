from pydantic import BaseModel

class LocationSchema(BaseModel):
    location_type_id :int
    location_name: str
    floor: int
    hotel_id: int

class LocationTypeSchema(BaseModel):
    location_type_name: str