from fastapi import HTTPException
from src.services.base import BaseService
from src.schemas.bookings import AddBookingsFromUser, AddBookings
from src.exceptions.exceptions import (
    ObjectNotFoundException,
    AllRoomsAreBookedException,
    RoomNotFoundHTTPException,
    RoomNotFoundException,
    check_date_to_after_date_from
)

class BookingService(BaseService):
    async def create_booking(
            self,
            data: AddBookingsFromUser,
            user_id: int,
    ) :
        check_date_to_after_date_from(date_from=data.date_from, date_to=data.date_to)
        # Вычисляем цену
        try:
            room = await self.db.rooms.get_one(id=data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        days: int = (data.date_to - data.date_from).days  # на сколько дней забронировано
        price = days * room.price
        # Вызываем специализированный метод на добалвение бронирований
        hotel = await self.db.hotels.get_one(id=room.hotel_id)
        booking_data = AddBookings(
            **AddBookingsFromUser.model_dump(data), user_id=user_id, price=price
        )
        bookings_returned = await self.db.bookings.add_booking(
            data=booking_data, hotel_id=hotel.id
        )
        return bookings_returned
    
    async def get_my_bookigns(
            self,
            user_id: int
    ) :
        return await self.db.bookings.get_all(user_id=user_id)
    
    async def get_all_bookings(
            self
    ) :
        return await self.db.bookings.get_all()