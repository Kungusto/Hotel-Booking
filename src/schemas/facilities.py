from pydantic import BaseModel

class Uslugi(BaseModel) :
    id: int
    title: str 
    
class UslugiAdd(BaseModel) :
    title: str
    
class RoomsFacilitiesAdd(BaseModel) :
    room_id: int
    facility_id: int
    
class RoomsFacilities(RoomsFacilitiesAdd) : 
    id: int
