from sqlalchemy import select, insert, func, update, delete

## Pydantic
from src.schemas.hotels import Hotel

# ошибки
from sqlalchemy.exc import NoResultFound

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository) :
    model = HotelsOrm 
    schema = Hotel
    
    async def get_all(self, location, title, limit, offset) :
        query = select(HotelsOrm)
        
        if title :
            query = query.filter(HotelsOrm.title.like(f'%{title}%')) 
        if location :
            query = query.filter(HotelsOrm.location.like(f'%{location}%'))
            
        query = (
                query
                .limit(limit)
                .offset(offset)
        )
        
        result = await self.session.execute(query)
        
        return  [self.schema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
        