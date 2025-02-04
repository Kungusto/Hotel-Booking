from fastapi import APIRouter, Request, Response
from src.schemas.bookings import AddBookingsFromUser, AddBookings
from src.api.dependencies import DBDep, GetUserId

from datetime import timedelta

router = APIRouter(prefix='/bookings', tags=['Бронирование'])

@router.post('/create_booking')
async def create_booking(data: AddBookingsFromUser, db: DBDep, user_id: GetUserId) : 
    time_of_booking = data.date_to - data.date_from
    price_for_one_day = await db.rooms.get_one_or_none(id=data.room_id)
    price = time_of_booking.days*price_for_one_day.price
    bookings_data = data.dict()
    bookings_data['user_id'], bookings_data['price'] = user_id, price
    booking_add = AddBookings(**bookings_data)
    bookings_returned = await db.bookings.add(data=booking_add)
    await db.commit()
    return bookings_returned