from sqlalchemy import insert, select
from pydantic import EmailStr
from src.exceptions.exceptions import UserAlreadyExistsException
from src.repositories.mappers.mappers import UserDataMapper
from src.repositories.mappers.base import DataMapper
from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import UserWithHashedPassword
from sqlalchemy.exc import IntegrityError

class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper: DataMapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model, from_attributes=True)
    
    async def add(self, data):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try : 
            result = await self.session.execute(add_stmt)
        except IntegrityError :
            raise UserAlreadyExistsException
        model = result.scalars().first()
        return self.mapper.map_to_domain_entity(model)