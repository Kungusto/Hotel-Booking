from fastapi import APIRouter, Response
from src.exceptions.exceptions import (
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
    WrongPasswordException,
    WrongPasswordHTTPException,
    ObjectNotFoundException,
)
from passlib.context import CryptContext
from src.services.auth import UsersService
from src.api.dependencies import DBDep
from src.schemas.users import UserRequestAdd, UserLogin
from src.api.dependencies import UserIdDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(data: UserRequestAdd, db: DBDep):
    try:
        hotel = await UsersService(db).register_user(data=data)
    except UserAlreadyExistsException as ex:
        raise UserAlreadyExistsHTTPException from ex
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.post("/login")
async def login_user(data: UserLogin, response: Response, db: DBDep):
    try:
        acces_token = await UsersService(db).login_user(data=data, response=response)
    except UserNotFoundException as ex:
        raise UserNotFoundHTTPException from ex
    except WrongPasswordException as ex:
        raise WrongPasswordHTTPException from ex
    except ObjectNotFoundException as ex:
        raise UserNotFoundHTTPException from ex
    return {"acces_token": acces_token}


@router.get("/me")
async def get_me(data: UserIdDep, db: DBDep):
    try:
        user = await UsersService(db).get_me_by_cookies(data=data)
    except UserNotFoundException as ex:
        raise UserNotFoundHTTPException from ex
    except WrongPasswordException as ex:
        raise WrongPasswordHTTPException from ex
    return user


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
