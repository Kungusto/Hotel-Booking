from fastapi import APIRouter, Request, Response
from fastapi.exceptions import HTTPException
from src.schemas.bookings import AddBookingsFromUser, AddBookings
from src.api.dependencies import DBDep, GetUserId
from datetime import timedelta

router = APIRouter(prefix='/bookings', tags=['Бронирование'])

@router.post('/create_booking')
async def create_booking(data: AddBookingsFromUser, db: DBDep, user_id: GetUserId) : 
    # Вычисляем цену
    price_for_one_day = await db.rooms.get_one_or_none(id=data.room_id)
    price = ((data.date_to - data.date_from)).days*price_for_one_day.price
    bookings_returned = await db.bookings.add_booking(
        AddBookings(
            **AddBookingsFromUser.model_dump(data),
            user_id=user_id,
            price=price
        )
    )
    await db.commit()
    return {"status":"OK", "data":bookings_returned}

@router.get('/me')
async def get_booking(user_id: GetUserId, db: DBDep) :
    return await db.bookings.get_all(user_id=user_id)

@router.get('')
async def get_booking(db: DBDep) :
    return await db.bookings.get_all()

