from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {'id':1, 'title':'Sochi', 'name':'sochi-hotel'},
    {'id':2, 'title':'Dubai', 'name':'dubai-hotel'},
]

@app.get('/hotels')
def function(
    title: str | None = Query(default=None, description='Название'),
    id: int | None = Query(default=None, description='Идентификатор')
) :
    _hotels = []

    for hotel in hotels:
        if id and hotel['id'] != id :
            continue
        if title and hotel['title'] != title :
            continue
        _hotels.append(hotel)

    return _hotels

@app.delete('/hotels/delete/{id_hotel}')
def delete_hotel(id_hotel: int) :
    for index, hotel in enumerate(hotels) :    
        if hotel['id'] == id_hotel :
            del hotels[index]
            return {'status':'OK'}
    return {'status':'Not Found'}

@app.post('/hotels')
def create_hotes(
    title: str = Body(embed=True)
) :
    hotels.append({
        'id' : hotels[-1]['id'] + 1,
        'title' : title
    })

    return {'status':'OK'}


@app.put("/hotels/{hotel_id}")
def edit_hotels(
    id: int = Body(),
    title: str = Body(),
    name: str = Body()
) : 
    for hotel in hotels :
        if hotel['id'] == id :
            hotel['title'], hotel['name'] = title, name
            return {'status':'OK'}
    return {'status':'Not Found'}

@app.patch("/hotels/{hotel_id}")
def edit_hotels_partialy(
    id: int = Body(),
    title: str | None = Body(),
    name: str | None = Body()
) : 
    new_values = {}

    if title :
        new_values['title'] = title
    
    if name :
        new_values['name'] = name

    for hotel in hotels :
        if hotel['id'] == id :
            hotel['title'], hotel['name'] = new_values.get('title', hotel['title']), new_values.get('name', hotel['name'])
            return {'status':'OK'}
    return {'status':'Not Found'}
