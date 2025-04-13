from datetime import timezone, timedelta, datetime
import jwt
from sqlalchemy.exc import NoResultFound
from src.exceptions.exceptions import (
    ObjectNotFoundException,
    UserNotFoundException,
    WrongPasswordException,
    ExpiredTokenException
)
from src.services.base import BaseService
from passlib.context import CryptContext
from src.config import settings
from src.schemas.users import UserAdd
from jwt.exceptions import ExpiredSignatureError


ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UsersService(BaseService):
    async def register_user(self, data: UserAdd):
        hashedpassword = AuthService().hash_password(data.password)
        new_user_data = UserAdd(
            email=data.email,
            hashedpassword=hashedpassword,
        )
        return await self.db.users.add(new_user_data)

    async def login_user(self, data, response):
        try:
            user = await self.db.users.get_user_with_hashed_password(email=data.email)
        except NoResultFound as ex:
            raise UserNotFoundException from ex
        if not AuthService().verify_password(data.password, user.hashedpassword):
            raise WrongPasswordException
        acces_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=acces_token)
        return acces_token

    async def get_me_by_cookies(self, data):
        try:
            user = await self.db.users.get_one(id=data["user_id"])
        except ObjectNotFoundException as ex:
            raise UserNotFoundException from ex
        return user


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try :
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except ExpiredSignatureError as ex :
            raise ExpiredTokenException from ex
