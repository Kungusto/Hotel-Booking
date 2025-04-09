from src.api.dependencies import DBDep, GetUserId
from src.exceptions.exceptions import (
    AllRoomsAreBookedException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    DepartureBeforeArrivalException,
    DepartureBeforeArrivalHTTPException,
    AllRoomsAreBookedHTTPException,
)
from src.services.bookings import BookingService
from fastapi import APIRouter
from src.schemas.bookings import AddBookingsFromUser

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("/create_booking")
async def create_booking(data: AddBookingsFromUser, db: DBDep, user_id: GetUserId):
    try:
        bookings_returned = await BookingService(db).create_booking(
            data=data, user_id=user_id
        )
    except DepartureBeforeArrivalException as ex:
        raise DepartureBeforeArrivalHTTPException from ex
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except AllRoomsAreBookedException as ex:
        raise AllRoomsAreBookedHTTPException from ex
    await db.commit()
    return {"status": "OK", "data": bookings_returned}


@router.get("/me")
async def get_my_bookings(user_id: GetUserId, db: DBDep):
    return await BookingService(db).get_my_bookigns(user_id=user_id)


@router.get("")
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_all_bookings()
