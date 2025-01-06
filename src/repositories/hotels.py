from sqlalchemy import select, insert, func, update, delete

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm

class HotelsRepository(BaseRepository) :
    model = HotelsOrm 
    
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
        
        return result.scalars().all()
    
    async def add(self, hotel_data) : 
        add_hotel_stmt = insert(self.model).values(**hotel_data.model_dump()).returning(self.model)
        result = await self.session.execute(add_hotel_stmt)
        return result.scalars().first()

    async def edit(self, data, **filter_by) -> None : 
        edit_hotel_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump())
        await self.session.execute(edit_hotel_stmt)
         
    async def delete(self, **filter_by) -> None : 
        edit_hotel_stmt = delete(self.model).filter_by(**filter_by)     
        await self.session.execute(edit_hotel_stmt)