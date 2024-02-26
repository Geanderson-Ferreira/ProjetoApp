from pydantic import BaseModel, validator
from typing import Optional

class OrderSchema(BaseModel):
    location_id: int
    order_type_id: int
    image_data: str
    description: str
    created_by_id: int
    status_id: int
    hotel_id: int
    
class FilterOrderSchema(BaseModel):
    id: Optional[int] = None
    location_id: Optional[int] = None
    order_type_id: Optional[int] = None
    image_data: Optional[str] = None
    description: Optional[str] = None
    created_by_id: Optional[int] = None
    status_id: Optional[int] = None
    hotel_id: Optional[int] = None
    
    @validator("id", "location_id", "order_type_id", "image_data", "description", "created_by_id", "status_id", "hotel_id", pre=True, always=True)
    def convert_optional_fields_to_none(cls, value):
        return None if not value else value
        #return value if value is not None and value != "" else None

class OrderTypeSchema(BaseModel):
    order_type_name : str
