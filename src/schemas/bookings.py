from pydantic import BaseModel
from datetime import date

class AddBookingsFromUser(BaseModel) : 
    room_id : int
    date_from : date
    date_to : date
    
class AddBookings(AddBookingsFromUser) :
    user_id: int 
    price: int
    