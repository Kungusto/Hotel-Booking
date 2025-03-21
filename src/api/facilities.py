import json

from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.utils.init import redis_manager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from src.schemas.facilities import Uslugi, UslugiAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix='/facilities', tags=['Удобства'])

@router.get('')
@cache(expire=10)
async def get_all_uslugi(db: DBDep) :
    return await db.uslugi.get_all()
    
@router.post('')
async def post_uslugi(db: DBDep, data: UslugiAdd) : 
        result = await db.uslugi.add(data=data)
        await db.commit()
        test_task.delay()
        return result