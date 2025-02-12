from fastapi import APIRouter
from src.api.dependencies import DBDep

from src.schemas.facilities import Uslugi

router = APIRouter(prefix='/facilities', tags=['Удобства'])

@router.get('')
async def get_all_facilites() :
    ...
    
@router.post('/add')
async def post_facilities(
        db: DBDep,
        data: Uslugi
    ) : 
        result = await db.uslugi.add(data=data)
        await db.commit()
        return result