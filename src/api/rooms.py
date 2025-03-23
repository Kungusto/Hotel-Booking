from fastapi import APIRouter, Body, HTTPException, Query
from datetime import date
from src.exceptions.exceptions import (
    DepartureBeforeArrivalException,
    ObjectNotFoundException,
    NoChangesException,
)
from src.schemas.rooms import (
    RoomAdd,
    RoomAddRequest,
    PUTRoom,
    PUTRoomAdd,
    PATCHRoomAdd,
    PATCHRoomRequest,
)
from src.schemas.facilities import RoomsFacilitiesAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.post("/create_room")
async def create_room(
    db: DBDep, hotel_id: int = Query(), data: RoomAddRequest = Body()
):
    data_to_add = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    try:
        room_data = await db.rooms.add(data_to_add)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")

    dates_for_facilities = [
        RoomsFacilitiesAdd(room_id=room_data.id, facility_id=id_fclty)
        for id_fclty in data.facilities_ids
    ]
    if dates_for_facilities:
        await db.facilities.add_bulk(dates_for_facilities)
    await db.commit()
    return {"status": "OK", "data": data}


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_hotel(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(examples="2025-02-10"),
    date_to: date = Query(examples="2025-02-17"),
):
    try:
        rooms = await db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    except DepartureBeforeArrivalException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)
    return rooms


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(
    hotel_id: int,
    db: DBDep,
    room_id: int,
):
    try:
        result = await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    return result


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_hotel(
    hotel_id: int, room_id: int, request: PATCHRoomRequest, db: DBDep
):
    _room_data_dict = request.model_dump(exclude_unset=True)
    data = PATCHRoomAdd(**_room_data_dict)
    try:
        await db.rooms.edit(data, is_patch=True, id=room_id)
    except NoChangesException:
        raise HTTPException(status_code=400, detail="Номера не существует")
    if "facilities_ids" in _room_data_dict:
        await db.facilities.set_room_facilities(
            room_id=room_id, facilities_ids=request.facilities_ids
        )
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(hotel_id: int, room_id: int, db: DBDep, request: PUTRoom):
    data = PUTRoomAdd(**request.model_dump(), hotel_id=hotel_id)
    try:
        await db.rooms.edit(data, id=room_id, hotel_id=hotel_id)
    except NoChangesException:
        raise HTTPException(status_code=400, detail="Номера не существует")
    await db.facilities.set_room_facilities(
        room_id=room_id, facilities_ids=request.facilities_ids
    )
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    except NoChangesException:
        raise HTTPException(status_code=400, detail="Номера не существует")
    await db.commit()
    return {"status": "OK"}
