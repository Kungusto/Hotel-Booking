from pydantic import BaseModel
from datetime import date

class AddBookingsFromUser(BaseModel) : 
    room_id : int
    date_from : date
    date_to : date
    
class AddBookings(BaseModel) :
    room_id : int
    date_from : date
    date_to : date
    user_id: int 
    price: int
    
class PATCHBookings(BaseModel) :
    room_id : int | None = None
    date_from : date | None = None
    date_to : date | None = None
    user_id: int  | None = None
    price: int | None = None

class PUTBookings(AddBookings) : ...