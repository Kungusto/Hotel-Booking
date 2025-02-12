from fastapi import APIRouter, Body
from src.api.dependencies import DBDep

from src.schemas.facilities import Uslugi, UslugiAdd

router = APIRouter(prefix='/facilities', tags=['Удобства'])

@router.get('')
async def get_all_uslugi(
    db: DBDep,
) :
    return await db.uslugi.get_all()
    
@router.post('')
async def post_uslugi(
        db: DBDep,
        data: UslugiAdd
    ) : 
        result = await db.uslugi.add(data=data)
        await db.commit()
        return result