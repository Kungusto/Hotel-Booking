from tests.conftest import get_db_null_pool
import pytest


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-03-21", "2025-03-23", 200),
        (1, "2025-03-21", "2025-03-23", 200),
        (1, "2025-03-21", "2025-03-23", 200),
        (1, "2025-03-21", "2025-03-23", 200),
        (1, "2025-03-21", "2025-03-23", 200),
        (1, "2025-03-21", "2025-03-23", 500),
    ],
)
async def test_add_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    authenticated_ac,
):
    response = await authenticated_ac.post(
        url="/bookings/create_booking",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == status_code
    if response.status_code == 200:
        res = response.json()
        assert res
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, num_of_booking",
    [
        (1, "2025-03-21", "2025-03-23", 1),
        (1, "2025-04-22", "2025-04-30", 2),
        (1, "2025-04-29", "2025-05-01", 3),
        (1, "2025-04-21", "2025-05-23", 4),
        (1, "2025-11-21", "2026-01-01", 5),
        (1, "2025-02-21", "2025-03-03", 6),
    ],
)
async def test_add_and_get_my_bookings(
    authenticated_ac, room_id, date_from, date_to, num_of_booking, delete_bookings
):
    response_post = await authenticated_ac.post(
        url="/bookings/create_booking",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response_post.status_code == 200
    response_get = await authenticated_ac.get(url="/bookings/me")
    bookings_now = response_get.json()
    assert response_get.status_code == 200
    assert isinstance(bookings_now, list)
    assert len(bookings_now) == num_of_booking
