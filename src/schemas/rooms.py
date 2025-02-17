from pydantic import BaseModel, Field

class RoomAddRequest(BaseModel) : 
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int
    facilities_ids: list[int] | None = None
    
class RoomAdd(BaseModel) : 
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int

class Room(RoomAdd) :
    id: int

class RoomID(BaseModel) :
    id : int
    
class PATCHRoom(BaseModel) : 
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids: list[int] | None = Field(None)
    
class PUTRoom(BaseModel) :
    hotel_id: int 
    title: str 
    description: str 
    price: int 
    quantity: int 
    facilities_ids: list[int]

class PATCHRoomAdd(BaseModel) : 
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    
class PUTRoomAdd(BaseModel) :
    hotel_id: int 
    title: str 
    description: str 
    price: int 
    quantity: int 

