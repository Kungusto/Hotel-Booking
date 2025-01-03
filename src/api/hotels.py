from fastapi import Body, Query, APIRouter, Depends
from schemas.hotels import HotelPATCH, Hotel
from src.api.dependencies import PaginationDep

router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get('')
def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description='Город'),
    id: int | None = Query(default=None, description='Идентификатор'),
) :
    pagination.page -= 1
    
    _hotels = []

    for hotel in hotels:
        if id and hotel['id'] != id :
            continue
        if title and hotel['title'] != title :
            continue
        _hotels.append(hotel)

    if pagination.page and pagination.per_page :
        return _hotels[pagination.per_page*pagination.page:pagination.per_page*(pagination.page+1)]
    
    return _hotels

@router.delete('/delete/{id_hotel}')
def delete_hotel(id_hotel: int) :
    for index, hotel in enumerate(hotels) :    
        if hotel['id'] == id_hotel :
            del hotels[index]
            return {'status':'OK'}
    return {'status':'Not Found'}

@router.post('')
def create_hotes(
    hotel_data: Hotel = Body(openapi_examples={
        '1':{'summary':'Сочи', 'value':
            {'title':'Сочи', 'name':'Sochi-hotel'}}
    })
) :
    hotels.append({
        'id' : hotels[-1]['id'] + 1,
        'title' : hotel_data.title,
        'name' : hotel_data.name
    })

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

