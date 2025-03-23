from fastapi import APIRouter
from src.api.dependencies import DBDep
from fastapi_cache.decorator import cache
from src.schemas.facilities import UslugiAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_all_uslugi(db: DBDep):
    return await db.uslugi.get_all()


@router.post("")
async def post_uslugi(db: DBDep, data: UslugiAdd):
    result = await db.uslugi.add(data=data)
    await db.commit()
    test_task.delay()
    return result
