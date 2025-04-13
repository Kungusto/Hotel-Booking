from pydantic import BaseModel, field_validator
from src.exceptions.exceptions import EmptyTitleFacility

class Uslugi(BaseModel):
    id: int
    title: str


class UslugiAdd(BaseModel):
    title: str
    
    @field_validator("title")
    @classmethod
    def is_title_empty(cls, value) : 
        if len(value.strip()) <= 1 :
            raise EmptyTitleFacility
        return value

class RoomsFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomsFacilities(RoomsFacilitiesAdd):
    id: int
