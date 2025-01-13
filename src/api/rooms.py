# импорт библиотек
from fastapi import APIRouter, Body

# база данныз и подключение к ней
from src.database import async_session_maker

# репозитории
from src.repositories.rooms import RoomsRepository

# схемы
from src.schemas.rooms import Room

router = APIRouter(prefix='/hotels', tags=['Номера'])

@router.post('/create_room')
async def create_room(
    data: Room = Body(openapi_examples={
        '1':{
            'summary':'3-х местный эконом', 
            'value': {
                'hotel_id':1,
                'title':'3-х местный эконом',
                'description':None,
                'price':4500,
                'quantity':3
            }
        }
    })
) : 
    async with async_session_maker() as session : 
        query = await RoomsRepository(session).add(data)
        await session.commit()
    
    return {'status':'OK', 'data':data}

@router.get('{hotel_id}/{room_id}')
async def get_room(
    hotel_id: int,
    room_id: int
) :
    async with async_session_maker() as session :
        get_room_stmt = await RoomsRepository(session).get_one_or_none(id=room_id)
    
    return get_room_stmt
        