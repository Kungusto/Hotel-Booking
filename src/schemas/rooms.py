from pydantic import BaseModel, Field
from src.schemas.facilities import Uslugi


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int = Field(examples=[1])
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class Room(RoomAdd):
    id: int


class RoomWithRels(Room):
    facilities: list[Uslugi]


class RoomID(BaseModel):
    id: int


class PATCHRoom(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


class PATCHRoomRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


class PUTRoom(BaseModel):
    title: str
    description: str
    price: int
    quantity: int
    facilities_ids: list[int] = []


class PUTRoomRequest(BaseModel):
    title: str
    description: str
    price: int
    quantity: int
    facilities_ids: list[int] = []


class PATCHRoomAdd(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class PUTRoomAdd(BaseModel):
    title: str
    description: str
    price: int
    quantity: int
