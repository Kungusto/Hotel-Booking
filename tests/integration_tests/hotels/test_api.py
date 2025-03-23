async def test_get_hotels(ac):
    response = await ac.get(
        url="/hotels", params={"date_from": "2024-08-01", "date_to": "2024-08-10"}
    )
    assert response.status_code == 200
