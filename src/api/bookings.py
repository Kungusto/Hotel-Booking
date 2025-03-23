from fastapi import APIRouter, HTTPException
from src.schemas.bookings import AddBookingsFromUser, AddBookings
from src.api.dependencies import DBDep, GetUserId
from src.exceptions.exceptions import (
    ObjectNotFoundException,
    AllRoomsAreBookedException,
)

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("/create_booking")
async def create_booking(data: AddBookingsFromUser, db: DBDep, user_id: GetUserId):
    # Вычисляем цену
    try:
        room = await db.rooms.get_one(id=data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    days: int = (data.date_to - data.date_from).days  # на сколько дней забронировано
    price = days * room.price
    # Вызываем специализированный метод на добалвение бронирований
    hotel = await db.hotels.get_one(id=room.hotel_id)
    booking_data = AddBookings(
        **AddBookingsFromUser.model_dump(data), user_id=user_id, price=price
    )
    try:
        bookings_returned = await db.bookings.add_booking(
            data=booking_data, hotel_id=hotel.id
        )
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": bookings_returned}


@router.get("/me")
async def get_my_bookings(user_id: GetUserId, db: DBDep):
    return await db.bookings.get_all(user_id=user_id)


@router.get("")
async def get_booking(db: DBDep):
    return await db.bookings.get_all()
