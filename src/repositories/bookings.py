from sqlalchemy import select

from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.utils import rooms_ids_for_booking

from datetime import date

class BookingsRepository(BaseRepository) : 
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self) : 
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [BookingDataMapper.map_to_domain_entity(model) for model in res.scalars().all()]

    async def get_available_room(self, hotel_id, date_to, date_from) -> list[int] :
        '''Возвращает свободные номера на данных'''
        test_data = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to,
            hotel_id=hotel_id
        )
        rooms = await self.session.execute(test_data)
        result = rooms.scalars().all()
        return result