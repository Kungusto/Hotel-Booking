from pydantic import BaseModel, EmailStr

class UserRequestAdd(BaseModel) : 
    email: EmailStr
    name: str
    nickname: str
    password: str
    
class UserAdd(BaseModel) : 
    email: EmailStr
    name: str
    nickname: str
    hashedpassword: str
    
class User(BaseModel) :
    id: int
    name: str
    nickname: str
    email: EmailStr

class UserLogin(BaseModel) :
    email: EmailStr
    password: str

class UserWithHashedPassword(User) :
    hashedpassword: str