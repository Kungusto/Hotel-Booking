from src.schemas.facilities import UslugiAdd
from src.config import settings

async def test_facilities_add(ac, db) :
    response = await ac.post(
        url="/facilities",
        json={
            "title" : "Вай-файййй в номере"
        }
    )
    print(response.json())
    facitilies = await db.facilities.get_all()
    print(facitilies)
    assert response.status_code == 200