from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os
# Загрузка настроек из .env-test, если MODE установлено в TEST
mode = os.getenv('MODE', 'LOCAL')
if mode == 'TEST':
    load_dotenv(".env-test", override=True)
else:
    load_dotenv(".env", override=True)
from src.config import settings # noqa: E402

engine = create_async_engine(settings.DB_URL)
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)

class Base(DeclarativeBase):
    pass