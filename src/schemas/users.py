from src.exceptions.exceptions import TooShortPasswordHTTPException, TooLongPasswordHTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRequestAdd(BaseModel):
    email: EmailStr 
    password: str = Field(examples=["Beautiful_password_2025"])

    @field_validator("password")
    @classmethod
    def password_is_not_empty(cls, value: str) : 
        if not value.strip() or len(value.strip()) < 12:
            raise TooShortPasswordHTTPException # Кастомные ошибки для HTTP-ответа
        if len(value.strip()) > 32 :
            raise TooLongPasswordHTTPException # Кастомные ошибки для HTTP-ответа
        return value

class UserAdd(BaseModel):
    email: EmailStr
    hashedpassword: str


class User(BaseModel):
    id: int
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserWithHashedPassword(User):
    hashedpassword: str
