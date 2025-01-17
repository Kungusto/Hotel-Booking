from sqlalchemy import select, update, delete, insert

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room

class RoomsRepository(BaseRepository) :
    model = RoomsOrm
    schema = Room
    
    async def get_all(self, hotel_id, title, price, quentity) : 
        get_rooms_stmt = insert(RoomsOrm)
            
        if hotel_id : 
            get_rooms_stmt = get_rooms_stmt.filter_by(hotel_id)
        if title : 
            get_rooms_stmt = get_rooms_stmt.filter_by(title)
        if price : 
            get_rooms_stmt = get_rooms_stmt.filter_by(price)
        if quentity : 
            get_rooms_stmt = get_rooms_stmt.filter_by(quentity)
            
        result = self.session.execute(get_rooms_stmt)    
            
        print(result.scalars().all())
            
        return result.scalars().all()
        
    
    
# id|hotel_id|title             |description|price|quantity|