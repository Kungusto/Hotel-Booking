from datetime import date
from sqlalchemy import select, func
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


def rooms_ids_for_booking(date_to: date, date_from: date, hotel_id: int | None = None):
    rooms_and_employed = (
        select(BookingsOrm.room_id, func.count("*").label("employed_rooms"))
        .select_from(BookingsOrm)
        .filter(BookingsOrm.date_from <= date_to, BookingsOrm.date_to >= date_from)
        .group_by(BookingsOrm.room_id)
        .cte(name="rooms_count")
    )

    rooms_free = (
        select(
            RoomsOrm.id.label("room_id"),
            (
                RoomsOrm.quantity
                - func.coalesce(rooms_and_employed.c.employed_rooms, 0)
            ).label("rooms_left"),
            RoomsOrm.hotel_id,
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_and_employed, rooms_and_employed.c.room_id == RoomsOrm.id)
    )

    rooms_ids_for_hotel = select(RoomsOrm.id).select_from(RoomsOrm)

    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel")

    result_request = (
        select(rooms_free.c.room_id)
        .select_from(rooms_free)
        .filter(
            rooms_free.c.rooms_left > 0,
            rooms_free.c.room_id.in_(select(rooms_ids_for_hotel)),
        )
    )

    return result_request
