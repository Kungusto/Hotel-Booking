from fastapi import APIRouter, HTTPException, Response, Request
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

# сервисы
from src.services.auth import AuthService

# схемы
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin

# репозитории
from src.repositories.users import UsersRepository

# базы данных и ORM
from src.database import async_session_maker

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

pwd_context = CryptContext(schemes=['bcrypt'],  deprecated='auto') 

@router.post('/register')
async def register_user(
    data: UserRequestAdd
) : 
    hashedpassword = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashedpassword=hashedpassword, name=data.name, nickname=data.nickname)
    try :
        async with async_session_maker() as session :
            hotel = await UsersRepository(session).add(new_user_data)
            await session.commit() 
    except IntegrityError  :
        raise HTTPException(status_code=422, detail='Пользователь с таким email уже существует!')
    
    return {'status':'OK'}

@router.post('/login') 
async def login_user(
    data: UserLogin,
    response: Response
) :
    async with async_session_maker() as session :
        user = await UsersRepository(session).get_user_with_hashed_password(email = data.email)

        if not user : 
            raise HTTPException(status_code=401, detail='Пользователя с таким email не существует')
        
        if not AuthService().verify_password(data.password, user.hashedpassword) :
            raise HTTPException(status_code=401, detail='Неверный пароль')
        
        acces_token = AuthService().create_access_token({'user_id':user.id})
        response.set_cookie(key='access_token', value=acces_token)
        return {'acces_token' : acces_token}

@router.get('/only_auth')
async def only_auth(
    request: Request
) :
    cookies = request.cookies
    
    access_token = cookies.get('access_token', None)
    
    print(access_token)
    
    return {'access_token':access_token}