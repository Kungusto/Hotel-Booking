from schemas.hotels import HotelAdd
from src.utils.dbmanager import DBManager
from src.database import async_session_maker_null_pool

async def test_add_hotel() : 
    data = HotelAdd(
        title="five stars",
        location="Москва"
    )
    async with DBManager(session_factory=async_session_maker_null_pool) as db :
        new_hotel_data = await db.hotels.add(data)
        await db.commit()

    assert new_hotel_data
