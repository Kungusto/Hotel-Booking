import pytest
from httpx import AsyncClient

from src.config import settings
from src.database import Base, engine_null_pool
from src.models import *
from src.main import app 

@pytest.fixture(scope="session", autouse=True)
async def async_main():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session", autouse=True)
async def register_user() : 
    async with AsyncClient(app=app, base_url="http://test") as ac : 
        await ac.post(
            url="/auth/register",
            json={
                "email":"John@example.com",
                "nickname":"John",
                "name":"John",
                "password":"John"
            })
