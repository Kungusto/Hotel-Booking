# импорт библиотек
from fastapi import APIRouter, Body, Query
from datetime import date

# база данныз и подключение к ней
from src.database import async_session_maker
from src.models.facilities import RoomsFacilitiesOrm

# репозитории
from src.repositories.rooms import RoomsRepository

# схемы
from src.schemas.rooms import Room, PATCHRoom, RoomAdd, RoomAddRequest, PUTRoom, PUTRoomAdd, PATCHRoomAdd
from src.schemas.facilities import RoomsFacilitiesAdd

from api.dependencies import DBDep

router = APIRouter(prefix='/hotels', tags=['Номера'])

@router.post('/create_room')
async def create_room(
    db: DBDep,
    hotel_id: int = Query(),
    data: RoomAddRequest = Body()
) : 
    data_to_add = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    room_data = await db.rooms.add(data_to_add)
    
    dates_for_facilities = [RoomsFacilitiesAdd(room_id=room_data.id, facility_id=id_fclty) for id_fclty in data.facilities_ids]
    await db.facilities.add_bulk(dates_for_facilities)
    
    await db.commit()
    
    return {'status':'OK', 'data':data}

    
@router.get('/{hotel_id}/rooms')
async def get_rooms_by_hotel(
    db: DBDep, 
    hotel_id: int,
    date_from: date = Query(example='2025-02-10'),
    date_to: date = Query(example='2025-02-17')
) :
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get('/{hotel_id}/{room_id}')
async def get_room_by_id(
    hotel_id: int,
    db: DBDep,
    room_id: int,
) :
    get_room_stmt = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    
    return get_room_stmt
        

# @router.get('/rooms')
# async def get_rooms(
#     hotel_id: int = Query(description='Идентификатор отеля'),
#     title: str | None = Query(default=None, description='Название номера'),
#     price : int | None = Query(default=None, description='Цена'),
#     quantity : int | None = Query(default=None, description='Вместимость номера')
# ) : 
#     async with async_session_maker() as session : 
#         query = await RoomsRepository(session).get_all(
#             title=title,
#             price=price, 
#             quantity=quantity,
#             hotel_id=hotel_id
#         )   
        
#     return query

@router.patch('/{hotel_id}/{room_id}')
async def patch_hotel(
    room_id: int,
    request: PATCHRoom, 
    db: DBDep
) : 
    data = PATCHRoomAdd(**request.model_dump(exclude_unset=True))
    await db.rooms.edit(data, is_patch=True, id=room_id)
    not_sorted_result = await db.facilities.get_filtered(room_id=room_id)
    
    all_fclts_ids = {model.facility_id for model in not_sorted_result}
    target_ids = set(request.facilities_ids)
    ids_to_delete = all_fclts_ids - target_ids
    ids_to_add = target_ids - all_fclts_ids
    await db.facilities.delete(
        RoomsFacilitiesOrm.facility_id.in_(list(ids_to_delete))
        ) # удаляем те, которых нету в новых удобствах
    data_to_add = [RoomsFacilitiesAdd(room_id=room_id, facility_id=fclt_id) for fclt_id in ids_to_add]
    if ids_to_add :
        await db.facilities.add_bulk(data_to_add) 
    await db.commit() 
    return {'status':'OK'}
        
@router.put('/{hotel_id}/{room_id}')
async def put_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
    request: PUTRoom
) : 
    data = PUTRoomAdd(**request.model_dump())
    await db.rooms.edit(data, id=room_id)
    not_sorted_result = await db.facilities.get_filtered(room_id=room_id)
    
    all_fclts_ids = {model.facility_id for model in not_sorted_result}
    target_ids = set(request.facilities_ids)
    ids_to_delete = all_fclts_ids - target_ids
    ids_to_add = target_ids - all_fclts_ids
    await db.facilities.delete(
        RoomsFacilitiesOrm.facility_id.in_(list(ids_to_delete))
        ) # удаляем те, которых нету в новых удобствах
    data_to_add = [RoomsFacilitiesAdd(room_id=room_id, facility_id=fclt_id) for fclt_id in ids_to_add]
    print(data_to_add)
    if ids_to_add :
        await db.facilities.add_bulk(data_to_add) 
    await db.commit() 

    return {'status':'OK'}

@router.delete('/{hotel_id}/{room_id}')
async def delete_room(
    hotel_id: int,
    room_id: int
) :
    async with async_session_maker() as session :
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    
    return {'status':'OK'}
