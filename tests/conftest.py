# ruff: noqa: E402, F403

# Установка переменной окружения MODE в TEST перед загрузкой настроек
from typing import Any, AsyncGenerator
from dotenv import load_dotenv
import os

os.environ["MODE"] = "TEST"
load_dotenv(".env-test", override=True)
# Мокаем декоратор кэш
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import json
import pytest
from httpx import ASGITransport, AsyncClient

from src.api.dependencies import get_db
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.dbmanager import DBManager
from src.config import Settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *
from src.main import app

settings = Settings()  # type: ignore


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, Any]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with DBManager(session_factory=async_session_maker_null_pool) as _db:
        with open("tests/mock_hotels.json", "r", encoding="utf-8") as file:
            data = [HotelAdd(**hotel) for hotel in json.load(file)]
            await _db.hotels.add_bulk(data)
        with open("tests/mock_rooms.json", "r", encoding="utf-8") as file:
            data = [RoomAdd(**room) for room in json.load(file)]
            await _db.rooms.add_bulk(data)
        await _db.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        url="/auth/register",
        json={
            "email": "John@example.com",
            "password": "JohnyCool_2010",
        },
    )


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac: AsyncClient):
    await ac.post(
        url="/auth/login", json={"email": "John@example.com", "password": "JohnyCool_2010"}
    )
    yield ac
