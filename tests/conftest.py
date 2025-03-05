import pytest
from httpx import AsyncClient, ASGITransport
from dotenv import load_dotenv
import os

# Установка переменной окружения MODE в TEST перед загрузкой настроек
os.environ['MODE'] = 'TEST'
load_dotenv(".env-test", override=True)

from src.config import Settings
from src.database import Base, engine_null_pool
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
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            url="/auth/register",
            json={
                "email": "John@example.com",
                "nickname": "John",
                "name": "John",
                "password": "John"
            }
        )
