from datetime import date
from sqlalchemy import select, insert, func, update, delete

# серсисы
from src.repositories.utils import rooms_ids_for_booking

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

    async def get_filtered_by_time(
        self, 
        date_from: date,
        date_to: date,
        location: str, 
        title: str,
        limit: int = 0, 
        offset: int = 5
    ) :

        rooms_stmt = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_stmt))
        )

        query = (
            select(HotelsOrm)
            .filter(HotelsOrm.id.in_(hotels_ids_to_get))
        )

        if title :
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower())) 
        if location :
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
            
        query = (
                query
                .limit(limit)
                .offset(offset)
        )
                
        result = await self.session.execute(query)
                
        return  [self.schema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]