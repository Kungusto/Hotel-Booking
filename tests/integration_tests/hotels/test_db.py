from schemas.hotels import HotelAdd
from src.utils.dbmanager import DBManager
from src.database import async_session_maker_null_pool

async def test_add_hotel(db) : 
    data = HotelAdd(
        title="five stars",
        location="Москва"
    )
    new_hotel_data = await db.hotels.add(data)
    assert new_hotel_data
    await db.commit()
