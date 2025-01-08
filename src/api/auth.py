from fastapi import APIRouter, HTTPException

from src.schemas.users import UserRequestAdd, UserAdd

from src.repositories.users import UsersRepository

from src.database import async_session_maker

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


from passlib.context import CryptContext

from sqlalchemy.exc import IntegrityError


pwd_context = CryptContext(schemes=['bcrypt'],  deprecated='auto')

@router.post('/register')
async def register_user(
    data: UserRequestAdd
) : 
    hashedpassword = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashedpassword=hashedpassword, name=data.name, nickname=data.nickname)
    try :
        async with async_session_maker() as session :
            hotel = await UsersRepository(session).add(new_user_data)
            await session.commit() 
    except IntegrityError  :
        raise HTTPException(status_code=422, detail='Пользователь с таким email уже существует!')
    
    return {'status':'OK'}
