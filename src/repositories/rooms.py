from sqlalchemy import Engine, func, select, update, delete, insert

from repositories.utils import rooms_ids_for_booking
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomID

from database import engine

class RoomsRepository(BaseRepository) :
    model = RoomsOrm
    schema = Room
    
    async def get_all(self, hotel_id, title, price, quantity) : 
        get_rooms_stmt = select(RoomsOrm)

        print(hotel_id, title, price, quantity)
            
        if hotel_id : 
            get_rooms_stmt = get_rooms_stmt.filter_by(hotel_id=hotel_id)
        if title : 
            get_rooms_stmt = get_rooms_stmt.filter_by(title=title)
        if price : 
            get_rooms_stmt = get_rooms_stmt.filter_by(price=price)
        if quantity : 
            get_rooms_stmt = get_rooms_stmt.filter_by(quantity=quantity)
            
        result = await self.session.execute(get_rooms_stmt)    
            
        return result.scalars().all()
    
    async def get_filtered_by_time(self, hotel_id, date_to, date_from) :
        result_request = rooms_ids_for_booking(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

        return await self.get_filtered(RoomsOrm.id.in_(result_request))