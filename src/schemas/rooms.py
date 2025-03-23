from pydantic import BaseModel, Field
from src.schemas.facilities import Uslugi

class RoomAddRequest(BaseModel) : 
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int
    facilities_ids: list[int] = []
    
class RoomAdd(BaseModel) : 
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int

class Room(RoomAdd) :
    id: int

class RoomWithRels(Room) :
    facilities: list[Uslugi] 

class RoomID(BaseModel) :
    id : int
    
class PATCHRoom(BaseModel) : 
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []

class PATCHRoomRequest(BaseModel) : 
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []
    
class PUTRoom(BaseModel) :
    hotel_id: int 
    title: str 
    description: str 
    price: int 
    quantity: int 
    facilities_ids: list[int] = []

class PUTRoomRequest(BaseModel) :
    title: str 
    description: str 
    price: int 
    quantity: int 
    facilities_ids: list[int] = []

class PATCHRoomAdd(BaseModel) : 
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    
class PUTRoomAdd(BaseModel) :
    hotel_id: int 
    title: str 
    description: str 
    price: int 
    quantity: int 

