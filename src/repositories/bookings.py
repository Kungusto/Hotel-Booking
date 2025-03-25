from datetime import date
from sqlalchemy import select
from src.schemas.bookings import AddBookings
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.exceptions.exceptions import AllRoomsAreBookedException


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        """Достать номера с сегодняшним заселением"""
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        res = await self.session.execute(query)
        return [
            BookingDataMapper.map_to_domain_entity(model)
            for model in res.scalars().all()
        ]

    async def get_available_room(self, hotel_id, date_to, date_from) -> list[int]:
        """Возвращает свободные номера на данных"""
        test_data = rooms_ids_for_booking(
            date_from=date_from, date_to=date_to, hotel_id=hotel_id
        )
        rooms = await self.session.execute(test_data)
        result = rooms.scalars().all()
        return result

    async def add_booking(self, data: AddBookings, hotel_id: int): 
        """Добавляет бронирование с учетом уже имеющихся"""
        # достаем номера, которые можно забронировать на этот интервал
        available_rooms: list[int] = await self.get_available_room(
            hotel_id, date_from=data.date_from, date_to=data.date_to
        )
        # проверяем, есть ли указанный пользователем номер в списке свободных
        if data.room_id in available_rooms:
            new_booking = await self.add(data=data)
            return new_booking
        raise AllRoomsAreBookedException
