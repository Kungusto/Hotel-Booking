from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotel
from database import engine

class BaseRepository :
    model = None
    mapper: DataMapper = None
    
    def __init__(self, session):
        self.session = session
    
    async def get_all(self, *args, **kwargs) : 
            query = (select(self.model))
            
            result = await self.session.execute(query)

            return  [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
        
    async def get_filtered(self, *filter, **filter_by) : 
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
         
        
    async def get_one_or_none(self, **filter_by) :
            query = select(self.model).filter_by(**filter_by)
            result = await self.session.execute(query)
            model = result.scalars().one_or_none()
            if model is None :
                return None 
            return  self.mapper.map_to_domain_entity(model)
                
    async def add(self, data) : 
        add_hotel_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_hotel_stmt)
        model = result.scalars().first()
        return  self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]) : 
        add_hotel_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_hotel_stmt)

    async def edit(self, data, is_patch=False, **filter_by) -> None : 
        edit_hotel_stmt = (
            (update(self.model)
             .filter_by(**filter_by)
             .values(**data.model_dump(exclude_unset=is_patch)))
        )
        await self.session.execute(edit_hotel_stmt)
         
    async def delete(self,*filter, **filter_by) -> None : 
        edit_hotel_stmt = (
            delete(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        await self.session.execute(edit_hotel_stmt)