from fastapi import APIRouter, HTTPException, Response, Request
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

# сервисы
from src.services.auth import AuthService
from src.api.dependencies import DBDep

# схемы
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.api.dependencies import UserIdDep

# репозитории
from src.repositories.users import UsersRepository

# базы данных и ORM
from src.database import async_session_maker

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

pwd_context = CryptContext(schemes=['bcrypt'],  deprecated='auto') 

@router.post('/register')
async def register_user(
    data: UserRequestAdd,
    db: DBDep
) : 
    hashedpassword = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashedpassword=hashedpassword, name=data.name, nickname=data.nickname)
    try :
        hotel = await db.users.add(new_user_data)
        await db.commit() 
    except IntegrityError  :
        raise HTTPException(status_code=422, detail='Пользователь с таким email уже существует!')
    
    return {'status':'OK', 'data':hotel}

@router.post('/login') 
async def login_user(
    data: UserLogin,
    response: Response,
    db: DBDep
) :
    user = await db.users.get_user_with_hashed_password(email = data.email)

    if not user : 
        raise HTTPException(status_code=401, detail='Пользователя с таким email не существует')
    if not AuthService().verify_password(data.password, user.hashedpassword) :
        raise HTTPException(status_code=401, detail='Неверный пароль')
    
    acces_token = AuthService().create_access_token({'user_id':user.id})
    response.set_cookie(key='access_token', value=acces_token)
    
    return {'acces_token' : acces_token}

@router.get('/me')
async def get_me(
    data: UserIdDep
) :
    async with async_session_maker() as session : 
        user = await UsersRepository(session).get_one_or_none(id=data['user_id'])
        return user

@router.post('/logout')
async def logout_user(
    response: Response
) :
    response.delete_cookie('access_token')
    return {'status':'OK'}