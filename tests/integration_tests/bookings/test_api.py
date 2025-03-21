from datetime import date
from src.schemas.bookings import AddBookingsFromUser

async def test_add_booking(authenticated_ac, db) :  
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        url="/bookings/create_booking",
        json={
            "room_id" : room_id, 
            "date_from" : "2025-03-21",
            "date_to" : "2025-03-23"
          }    
    )
    booking = await db.bookings.get_all()
    assert booking
    