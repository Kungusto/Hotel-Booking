from pydantic import BaseModel, Field

class Room(BaseModel) : 
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int

class GetRoom(Room) :
    id: int

class PATCHRoom(BaseModel) : 
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)

class PUTRoom(BaseModel) :
    hotel_id: int 
    title: str 
    description: str 
    price: int 
    quantity: int 