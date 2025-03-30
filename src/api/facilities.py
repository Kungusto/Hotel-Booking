from fastapi import APIRouter
from src.api.dependencies import DBDep
from fastapi_cache.decorator import cache
from src.schemas.facilities import UslugiAdd
from src.tasks.tasks import test_task
from src.services.facilities import FacilitiesService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_all_uslugi(db: DBDep):
    return await FacilitiesService(db).get_all_uslugi()


@router.post("")
async def post_uslugi(db: DBDep, data: UslugiAdd):
    return await FacilitiesService(db).add_uslugi(data)
