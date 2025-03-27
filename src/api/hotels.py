import logging
from src.exceptions.exceptions import (
    DepartureBeforeArrivalException,
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
    check_date_to_after_date_from
)
from datetime import date
from fastapi import Body, HTTPException, Query, APIRouter
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep
from src.api.dependencies import DBDep
from fastapi_cache.decorator import cache
from src.services.hotels import HotelSevice
from src.exceptions.exceptions import DepartureBeforeArrivalException

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(default=None, description="Город"),
    location: str | None = Query(default=None, description="Адрес"),
    date_from: date = Query(examples="2025-02-08"),
    date_to: date = Query(examples="2025-02-15"),
):
    try :
        return await HotelSevice(db).get_hotels_filtered_by_time(
                title=title,
                location=location,
                date_from=date_from,
                date_to=date_to,
                pagination=pagination,
            )
    except DepartureBeforeArrivalException as ex : 
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда") from ex
    
@router.get(
    path="/{hotel_id}",
    description="<h1>Получаем отель по id<h1>",
    summary="Получение отеля по id",
)
@cache(expire=30)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelSevice(db).hotel_by_id(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

@router.post("")
async def create_hotels(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Сочи", "location": "Ул. Моря, 2"},
            },
            "2": {
                "summary": "Урюпинск",
                "value": {
                    "title": "Урюпинск-Хостел",
                    "location": "Улица где гаснут фонари",
                },
            },
        }
    ),
):
    hotel = await HotelSevice(db).add_hotel(data=hotel_data)
    return {"status": "OK", "data": hotel}


@router.delete("/delete/{id_hotel}")
async def delete_hotel(id_hotel: int, db: DBDep):
    filters = {"id": id_hotel}
    try:
        await db.hotels.delete(**filters)
        await db.commit()
        return {"status": "OK"}
    except Exception as ex:
        logging.error(f"Произошла непредвиденная ошибка: {ex}")
        return {"status": "Not Found"}




@router.put(
    path="/{hotel_id}",
    summary="Полное изменение данных об отеле",
    description="Тут мы изменяем данные об отеле",
)
async def edit_hotels(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    filters = {"id": hotel_id}

    try:
        await db.hotels.edit(hotel_data, **filters)
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        print(e)
        return {"status": "Not Found"}


@router.patch(
    path="/{hotel_id}",
    summary="Частичное изменение данных об отеле",
    description="<h1>Тут мы частично изменяем данные об отеле</h1>",
)
async def edit_hotels_partialy(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    try:
        await db.hotels.edit(hotel_data, is_patch=True, id=hotel_id)
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        print(e)
        return {"status": "Not Found"}
