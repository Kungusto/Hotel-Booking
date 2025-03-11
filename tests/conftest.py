import json
import pytest
from httpx import ASGITransport, AsyncClient

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd

from dotenv import load_dotenv
import os
# Установка переменной окружения MODE в TEST перед загрузкой настроек
os.environ['MODE'] = 'TEST'
load_dotenv(".env-test", override=True)

from src.database import async_session_maker
from src.utils.dbmanager import DBManager
from src.config import Settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *
from src.main import app

settings = Settings()

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session", autouse=True)
async def register_user() : 
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac : 
        await ac.post(
            url="/auth/register",
            json={
                "email":"John@example.com",
                "nickname":"John",
                "name":"John",
                "password":"John"
            })

@pytest.fixture(scope="session", autouse=True)
async def complation_db_hotel() : 
    async with DBManager(session_factory=async_session_maker_null_pool) as db :
        with open('tests/mock_hotels.json', 'r', encoding='utf-8') as file : 
            data = [HotelAdd(**hotel) for hotel in json.load(file)] 
            await db.hotels.add_bulk(data)
        await db.commit()

@pytest.fixture(scope="session", autouse=True)
async def complation_db_rooms() : 
    async with DBManager(session_factory=async_session_maker_null_pool) as db :
        with open('tests/mock_rooms.json', 'r', encoding='utf-8') as file : 
            data = [RoomAdd(**room) for room in json.load(file)] 
            await db.rooms.add_bulk(data)
        await db.commit()
