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

    async def get_available_room(self) -> list[int] :
        '''Возвращает свободные номера на данный момент'''
        test_data = rooms_ids_for_booking(
            date_from=date(year=2024, month=12, day=25),
            date_to=date(year=2025, month=2, day=15),
            hotel_id=1
        )
        result = await self.session.execute(test_data)
        return result.scalars().all()