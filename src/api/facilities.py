from fastapi import APIRouter
from src.api.dependencies import DBDep

from src.schemas.facilities import Uslugi

router = APIRouter(prefix='/facilities', tags=['Удобства'])

@router.get('')
async def get_all_uslugi(
    db: DBDep,
) :
    return await db.uslugi.get_all()
    
@router.post('')
async def post_uslugi(
        db: DBDep,
        data: Uslugi
    ) : 
        result = await db.uslugi.add(data=data)
        await db.commit()
        return result