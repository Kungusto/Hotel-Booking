from pydantic import BaseModel
from fastapi import Query, Depends, Request, HTTPException
from typing import Annotated

from src.utils.dbmanager import DBManager
from src.services.auth import AuthService
from src.database import async_session_maker

class PaginationParams(BaseModel) :
    page: Annotated[int | None, Query(default=1, ge=1, lt=100),]
    per_page: Annotated[int | None, Query(default=5, ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str: 
    token = request.cookies.get('access_token', None)    
    if not token : 
        raise HTTPException(status_code=401, detail='Вы не аутентифицированы')
    return token

def get_current_user_id(request: Request, token = Depends(get_token)) : 
    cookies = request.cookies   
    token = cookies.get('access_token', None)    
    data = AuthService().decode_token(token)
    return data
    


UserIdDep = Annotated[int, Depends(get_current_user_id)]

def get_db_manager() :
    return DBManager(session_factory=async_session_maker)

async def get_db() :
    async with get_db_manager() as db : 
        yield db
        
DBDep = Annotated[DBManager, Depends(get_db)]

def get_id_user(token_dict = Depends(get_current_user_id)) :
    return token_dict['user_id']
    
GetUserId = Annotated[int, Depends(get_id_user)]