import logging
from fastapi import APIRouter, Body, Query
from datetime import date
from src.exceptions.exceptions import (
    DepartureBeforeArrivalException,
    ObjectNotFoundException,
    OutOfRangeException,
    UslugiNotFoundException,
    UslugiNotFoundHTTPException,
    OutOfRangeHTTPException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    DepartureBeforeArrivalHTTPException,
    InternalServerErrorHTTPException,
    RoomHasBookingsError,
    RoomHasBookingsHTTPException,
)
from src.schemas.rooms import (
    RoomAddRequest,
    PUTRoom,
    PATCHRoomRequest,
)
from src.services.rooms import RoomsService
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_hotel(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(examples="2025-02-10"),
    date_to: date = Query(examples="2025-02-17"),
):
    try:
        rooms = await RoomsService(db).get_room_by_date_and_hotel(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    except DepartureBeforeArrivalException as ex:
        raise DepartureBeforeArrivalHTTPException from ex
    except Exception as ex:
        logging.error(f"!! НЕПРЕДВИДЕННАЯ Ошибка: {type(ex).__name__}")
        logging.exception(ex)
        raise InternalServerErrorHTTPException from ex
    return rooms


@router.post("/create_room")
async def create_room(
    db: DBDep, hotel_id: int = Query(), data: RoomAddRequest = Body()
):
    try:
        await RoomsService(db).add_room_with_rels(hotel_id=hotel_id, data=data)
    except UslugiNotFoundException as ex:
        raise UslugiNotFoundHTTPException from ex
    except ObjectNotFoundException as ex:
        raise ObjectNotFoundException from ex
    except OutOfRangeException as ex:
        raise OutOfRangeHTTPException from ex
    except Exception as ex:
        logging.error(f"!! НЕПРЕДВИДЕННАЯ Ошибка: {type(ex).__name__}")
        logging.exception(ex)
        raise InternalServerErrorHTTPException from ex
    await db.commit()
    return {"status": "OK", "data": data}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(
    hotel_id: int,
    db: DBDep,
    room_id: int,
):
    try:
        result = await RoomsService(db).get_room_by_id(
            hotel_id=hotel_id, room_id=room_id
        )
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    except OutOfRangeException as ex:
        raise OutOfRangeHTTPException from ex
    except Exception as ex:
        logging.error(f"!! НЕПРЕДВИДЕННАЯ Ошибка: {type(ex).__name__}")
        logging.exception(ex)
        raise InternalServerErrorHTTPException from ex
    return result


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(hotel_id: int, room_id: int, request: PATCHRoomRequest, db: DBDep):
    try:
        await RoomsService(db).patch_room_with_rels(
            hotel_id=hotel_id, room_id=room_id, request=request
        )
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except UslugiNotFoundException as ex:
        raise UslugiNotFoundHTTPException from ex
    except OutOfRangeException as ex:
        raise OutOfRangeHTTPException from ex
    except Exception as ex:
        logging.error(f"!! НЕПРЕДВИДЕННАЯ Ошибка: {type(ex).__name__}")
        logging.exception(ex)
        raise InternalServerErrorHTTPException from ex
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(hotel_id: int, room_id: int, db: DBDep, request: PUTRoom):
    try:
        await RoomsService(db).put_room_with_rels(
            hotel_id=hotel_id, room_id=room_id, request=request
        )
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except UslugiNotFoundException as ex:
        raise UslugiNotFoundHTTPException from ex
    except OutOfRangeException as ex:
        raise OutOfRangeHTTPException from ex
    except Exception as ex:
        logging.error(f"!! НЕПРЕДВИДЕННАЯ Ошибка: {type(ex).__name__}")
        logging.exception(ex)
        raise InternalServerErrorHTTPException from ex
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomsService(db).delete_room(room_id=room_id, hotel_id=hotel_id)
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except RoomHasBookingsError as ex:
        raise RoomHasBookingsHTTPException from ex
    except OutOfRangeException as ex:
        raise OutOfRangeHTTPException from ex
    except Exception as ex:
        logging.error(f"!! НЕПРЕДВИДЕННАЯ Ошибка: {type(ex).__name__}")
        logging.exception(ex)
        raise InternalServerErrorHTTPException from ex
    await db.commit()
    return {"status": "OK"}
