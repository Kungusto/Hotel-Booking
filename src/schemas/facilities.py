from pydantic import BaseModel

class Uslugi(BaseModel) :
    id: int
    title: str 
    
class RoomsFacilities(BaseModel) :
    id: int
    room_id: int
    facility_id: int