from datetime import date
from sqlalchemy import select, insert, func, update, delete

## Pydantic
from repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel

# ошибки
from sqlalchemy.exc import NoResultFound

# БД
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm

class HotelsRepository(BaseRepository) :
    model = HotelsOrm 
    schema = Hotel

# ---------------------------------------------------- #
    async def get_filtered_by_time(
        self, 
        date_from: date,
        date_to: date,
        location: str, 
        title: str,
        limit: int = 0, 
        offset: int = 5
    ) :
        filters_by = {}
        
        if location : 
            filters_by['location'] = location
        if title : 
            filters_by['title'] = title
        
        rooms_stmt = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to)
        
        hotels_id_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_stmt))
        )
        return (await self.get_filtered(HotelsOrm.id.in_(hotels_id_to_get),
                **filters_by
            ))[offset:offset+limit]
# ---------------------------------------------------- #