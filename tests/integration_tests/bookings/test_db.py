from src.schemas.bookings import AddBookings, PATCHBookings
from src.utils.dbmanager import DBManager
from datetime import date

async def test_booking_crud(db: DBManager) : 
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    data_to_add = AddBookings(
        room_id=room_id, 
        user_id=user_id,
        date_from=date(year=2024, month=12, day=25),
        date_to=date(year=2025, month=1, day=1),
        price=10000
    )
    new_booking_data = await db.bookings.add(data_to_add)
    assert new_booking_data
    assert new_booking_data.model_dump() == data_to_add.model_dump()

    # Прочитать
    booking_data = await db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)
    assert booking_data.model_dump() == data_to_add.model_dump()

    # Обновить 
    data_to_edit = PATCHBookings(
        date_from=date(year=2024, month=12, day=25),
        date_to=date(year=2025, month=2, day=15),
        price=15000
    )
    await db.bookings.edit(data_to_edit, is_patch=True, user_id=user_id, room_id=room_id)
    booking_data = await db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)
    assert booking_data
    assert {'date_from' : booking_data.date_from, 
            'date_to' : booking_data.date_to,
              'price' : booking_data.price} == {'date_from' : data_to_edit.date_from, 
            'date_to' : data_to_edit.date_to,
              'price' : data_to_edit.price}

    # Удалить
    await db.bookings.delete(user_id=user_id, room_id=room_id)
    booking_data = await db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)
    assert not booking_data

    await db.commit()




