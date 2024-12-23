from fastapi import Body, Query, APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {'id':1, 'title':'Sochi', 'name':'sochi-hotel'},
    {'id':2, 'title':'Dubai', 'name':'dubai-hotel'},
]

class Hotel(BaseModel) :
    title: str
    name: str

@router.get('')
def function(
    title: str | None = Query(default=None, description='Город'),
    name: str | None = Query(default=None, description='Имя отеля'),
    id: int | None = Query(default=None, description='Идентификатор')
) :
    _hotels = []

    for hotel in hotels:
        if id and hotel['id'] != id :
            continue
        if title and hotel['title'] != title :
            continue
        if name and hotel['name'] != name :
            continue
        _hotels.append(hotel)

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
    hotel_data: Hotel
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
    title: str | None = Body(),
    name: str | None = Body()
) : 
    new_values = {}

    if title :
        new_values['title'] = title
    
    if name :
        new_values['name'] = name

    for hotel in hotels :
        if hotel['id'] == hotel_id :
            hotel['title'], hotel['name'] = new_values.get('title', hotel['title']), new_values.get('name', hotel['name'])
            return {'status':'OK'}
    return {'status':'Not Found'}

