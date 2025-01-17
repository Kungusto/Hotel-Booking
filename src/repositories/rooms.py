from sqlalchemy import select, update, delete, insert

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room

class RoomsRepository(BaseRepository) :
    model = RoomsOrm
    schema = Room
    
    async def get_all(self, hotel_id, title, price, quantity) : 
        get_rooms_stmt = select(RoomsOrm)

        print(quantity)
            
        if hotel_id : 
            get_rooms_stmt = get_rooms_stmt.filter_by(hotel_id=hotel_id)
        if title : 
            get_rooms_stmt = get_rooms_stmt.filter_by(title=title)
        if price : 
            get_rooms_stmt = get_rooms_stmt.filter_by(price=price)
        if quantity : 
            get_rooms_stmt = get_rooms_stmt.filter_by(quantity=quantity)
            
        result = await self.session.execute(get_rooms_stmt)    
            
        print(str(get_rooms_stmt))
            
        return result.scalars().all()
        
    
    
# id|hotel_id|title             |description|price|quantity|