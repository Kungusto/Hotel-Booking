from fastapi import Body, Query, APIRouter, Depends

from src.schemas.hotels import HotelPATCH, Hotel
from src.api.dependencies import PaginationDep

# импорт orm
from src.database import async_session_maker
from src.models.hotels import HotelsOrm

from sqlalchemy import *

router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = {}

@router.get('')
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description='Город'),
    location: str | None = Query(default=None, description='Адрес'),
) :
    
    async with async_session_maker() as session :
        query = select(HotelsOrm)
        
        if title :
            query = query.filter(HotelsOrm.title.like(f'%{title}%')) 
        if location :
            query = query.filter(HotelsOrm.location.like(f'%{location}%'))
            
        query = (
                query.
                limit(pagination.per_page).
                offset(pagination.per_page * (pagination.page - 1))
        )

        
        result = await session.execute(query)
        hotels = result.scalars().all()
        
        return hotels


        # if pagination.page and pagination.per_page :
        #     return _hotels[pagination.per_page*pagination.page:pagination.per_page*(pagination.page+1)]
        
        

@router.delete('/delete/{id_hotel}')
def delete_hotel(id_hotel: int) :
    for index, hotel in enumerate(hotels) :    
        if hotel['id'] == id_hotel :
            del hotels[index]
            return {'status':'OK'}
    return {'status':'Not Found'}

@router.post('')
async def create_hotels(
    hotel_data: Hotel = Body(openapi_examples={
        '1':{'summary':'Сочи', 'value':
            {'title':'Сочи', 'location':'Ул. Моря, 2'}},
        '2':{'summary':'Урюпинск', 'value':
             {'title':'Урюпинск-Хостел', 'location':'Улица где гаснут фонари'}}
    })
) :
    async with async_session_maker() as session :
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit() 

    return {'status':'OK'}

@router.put(
    path="/{hotel_id}", 
    summary='Полное изменение данных об отеле', 
    description='Тут мы изменяем данные об отеле')
def edit_hotels(hotel_id: int, hotel_data: Hotel) : 
    print(f'id: {hotel_id}')
    for hotel in hotels :
        print(hotel['id'], hotel_id)
        if hotel['id'] == hotel_id :
            hotel['title'], hotel['name'] = hotel_data.title, hotel_data.name
            return {'status':'OK'}
    return {'status':'Not Found'}

@router.patch(path="/{hotel_id}", 
           summary='Частичное изменение данных об отеле', 
           description='<h1>Тут мы частично изменяем данные об отеле</h1>')
def edit_hotels_partialy(
    hotel_id: int,
    hotel_data: HotelPATCH
) : 
    new_values = {}

    if hotel_data.title :
        new_values['title'] = hotel_data.title
    
    if hotel_data.name :
        new_values['name'] = hotel_data.name

    for hotel in hotels :
        if hotel['id'] == hotel_id :
            hotel['title'], hotel['name'] = new_values.get('title', hotel['title']), new_values.get('name', hotel['name'])
            return {'status':'OK'}
    return {'status':'Not Found'}

