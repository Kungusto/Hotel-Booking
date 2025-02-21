from sqlalchemy import select

from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm

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