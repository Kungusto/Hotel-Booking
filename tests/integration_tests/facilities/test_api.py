from src.schemas.facilities import UslugiAdd
from src.config import settings
import json

async def test_facilities_add(ac, db) :
    response = await ac.post(
        url="/facilities",
        json={
            "title" : "Вай-фай в номере"
        }
    )
    facitilies = await db.uslugi.get_filtered(title="Вай-фай в номере")
    assert response.status_code == 200
    assert facitilies

    response = await ac.get(
        url="/facilities"
    )
    assert response.status_code == 200