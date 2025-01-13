from pydantic import BaseModel, Field

class Room(BaseModel) : 
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int

class GetRoom(Room) :
    id: int
