from sqlalchemy import Engine, func, select, update, delete, insert
from sqlalchemy.orm import selectinload, joinedload

from src.repositories.mappers.mappers import RoomDataMapper, RoomDataMapperWithRels
from repositories.utils import rooms_ids_for_booking
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import RoomAdd, RoomID, Room, RoomWithRels

from database import engine

class RoomsRepository(BaseRepository) :
    model = RoomsOrm
    mapper = RoomDataMapper
    
    async def get_all(self, hotel_id, title, price, quantity) : 
        get_rooms_stmt = select(RoomsOrm)

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
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(result_request))
        )
        print(query.compile())
        result = await self.session.execute(query)
        return [RoomDataMapperWithRels.map_to_domain_entity(model) for model in result.unique().scalars().all()]
    
    async def get_one_or_none_with_rels(self, **filter_by) :
        query = (
                select(self.model)
                .options(joinedload(self.model.facilities))
                .filter_by(**filter_by)
            )
        result = await self.session.execute(query)
        model = result.unique().scalars().one_or_none()
        if model is None :
            return None 
        return RoomDataMapperWithRels.map_to_domain_entity(model)
    