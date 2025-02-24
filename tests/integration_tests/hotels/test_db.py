from schemas.hotels import HotelAdd
from src.api.dependencies import get_db

async def test_add_hotel() : 
    data = HotelAdd(
        title="five stars",
        location="Москва"
    )
    async for db in get_db() :
        new_hotel_data = await db.hotels.add(data)
        await db.commit()

    assert new_hotel_data
