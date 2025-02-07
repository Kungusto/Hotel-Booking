from sqlalchemy import Engine, func, select, update, delete, insert

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomID

from database import engine

class RoomsRepository(BaseRepository) :
    model = RoomsOrm
    schema = RoomID
    
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
        rooms_count = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_from,
                BookingsOrm.date_to >= date_to
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )

        # CTE для расчета оставшихся свободных комнат
        rooms_left_table = (
            select(
                RoomsOrm.id.label("room_id"),
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left")
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )

        # Подзапрос для получения ID комнат в указанном отеле
        rooms_ids_for_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery(name="rooms_ids_for_hotel")
        )

        # Основной запрос для получения ID комнат, которые свободны
        rooms_ids_to_get = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotel)
            )
        )
            
        # Логирование SQL-запроса (для отладки)
        print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        # Возврат отфильтрованных комнат
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))